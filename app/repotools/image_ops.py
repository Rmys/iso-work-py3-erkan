#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import subprocess
import stat
import tempfile
import dbus
from .utility import wait_bus, run, xterm_title, strip_ansi

bus = None

def run_batch(cmd, shell=True, env=os.environ.copy()):
    proc = subprocess.Popen(cmd, shell=shell, env=env,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    for line in iter(proc.stdout.readline, b''):
        try:
            decoded_line = line.decode('utf-8', errors='ignore')
            print(strip_ansi(decoded_line), end='')
        except Exception as e:
            print(e)
    # print(proc.stderr.read().decode('utf-8', errors='ignore'))
    proc.poll()
    return proc.returncode

def overlay(project, path, to=None, upperdir=None, workdir=None):
    image_dir = project.image_dir()
    work_dir = project.work_dir
    overlay_dir = "{}/overlay".format(work_dir)

    if to is None:
        to = "{image_dir}/{path}".format(image_dir=image_dir, path=path)

    if upperdir is None:
        upperdir = "{}/upper_{}".format(overlay_dir, path)

    if workdir is None:
        workdir = "{}/work_{}".format(overlay_dir, path)

    for i in (overlay_dir, upperdir, workdir, to,):
        os.makedirs(i, exist_ok=True)

    run('/bin/mount -t overlay overlay -o lowerdir=/{path},upperdir={upperdir},workdir={workdir} {to}'.format(path=path, upperdir=upperdir, workdir=workdir, to=to))

def unoverlay(project, name, ignore_error=True):
    run('/bin/umount %s' % os.path.join(project.image_dir(), name), ignore_error=ignore_error)

def connectToDBus(path):
    global bus
    if os.environ.get('DBUS_SYSTEM_BUS_ADDRESS'):
        del os.environ['DBUS_SYSTEM_BUS_ADDRESS']
    os.environ['DBUS_SYSTEM_BUS_ADDRESS'] = "unix:path=%s/run/dbus/system_bus_socket" % path
    while True:
        try:
            bus = dbus.SystemBus()
            return bus
        except Exception as e:
            print("trying to connect dbus..")
            # print(e)
            time.sleep(1)

def chroot_comar(image_dir):
    print("DEBUG: Setting up D-Bus in chroot: %s" % image_dir)
    # Ensure /etc/passwd and /etc/group exist, otherwise DBus/COMAR won't start
    print("DEBUG: Setting up D-Bus/COMAR in chroot: %s" % image_dir)
    os.makedirs(os.path.join(image_dir, "etc"), exist_ok=True)
    # Copy essential auth files if missing or for safety
    for f in ['passwd', 'group', 'hosts', 'resolv.conf']:
        src = os.path.join('/etc', f)
        dst = os.path.join(image_dir, 'etc', f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print("DEBUG: Copied %s to chroot" % f)

    # Ensure /var/run -> /run link exists for legacy apps like pisi
    var_run = os.path.join(image_dir, "var/run")
    # os.system('rm -rf "%s"' % var_run) # Removed this hanging rm -rf
    try:
        # Link inside chroot must be relative to work both inside and outside
        os.symlink("../run", var_run)
        print("DEBUG: Created symlink %s -> ../run" % var_run)
    except OSError as e:
        print("DEBUG: Symlink error: %s" % e)
    
    os.makedirs(os.path.join(image_dir, "run/dbus"), exist_ok=True)
    os.makedirs(os.path.join(image_dir, "var/lib/dbus"), exist_ok=True)
    os.system('rm -f "%s"' % os.path.join(image_dir, "run/dbus/pid"))
    
    # Ensure machine-id
    if not os.path.exists(os.path.join(image_dir, "var/lib/dbus/machine-id")):
        run('chroot "%s" /usr/bin/dbus-uuidgen --ensure' % image_dir, ignore_error=True)
        
    # Start D-Bus
    print("DEBUG: Starting dbus-daemon via chroot command")
    # Setting DBUS_USER to root helps if nss is still tricky, but --system normally drops to dbus user
    run('chroot "%s" /usr/bin/dbus-daemon --system --fork --address=unix:path=/var/run/dbus/system_bus_socket' % image_dir, ignore_error=True)
    
    # Start COMAR
    if os.path.exists(os.path.join(image_dir, "usr/sbin/comard")):
        print("DEBUG: Starting comard via chroot command")
        run('chroot "%s" /usr/sbin/comard' % image_dir, ignore_error=True)
        
    socket_on_host = os.path.join(image_dir, "var/run/dbus/system_bus_socket")
    print("DEBUG: Waiting for socket: %s" % socket_on_host)
    if wait_bus(socket_on_host):
        print("DEBUG: D-Bus socket is READY on host.")
    else:
        print("DEBUG: D-Bus socket TIMEOUT on host!")

def get_exclude_list(project):
    excludes = [
        "var/cache/pisi/packages/*",
        "var/lib/pisi/index/*",
        "var/lib/pisi/scripts/*",
        "var/cache/pisi/archives/*"
    ]
    # Add more excludes from project if needed
    return excludes

def install_packages(project):
    image_dir = project.image_dir()
    if 'Calamares' in project.all_packages:
        packages = project.all_packages
    else:
        packages = project.all_install_image_packages
    
    run('pisi --yes-all --ignore-comar --ignore-dependency \
        --ignore-file-conflicts -D"%s" it %s \
        ' % (image_dir, " ".join(packages)))

def squash_image(project):
    from app.repotools.iso_ops import mkinitcpio
    image_dir = project.image_dir()
    image_file = project.image_file()

    mkinitcpio(project)

    print("squashfs image dir %s" % image_dir)
    if not image_dir.endswith("/"):
        image_dir += "/"
    
    temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
    temp.write("\n".join(get_exclude_list(project)))
    temp.close()

    mksquashfs_cmd = 'mksquashfs "%s" "%s" -noappend -comp %s -ef "%s"' % (
        image_dir, image_file, project.squashfs_comp_type, temp.name)
    run(mksquashfs_cmd)
    os.unlink(temp.name)

    with open(os.path.join(project.work_dir, "finished.txt"), 'w') as _file:
        _file.write("pack-live")

def make_image(project):
    global bus
    print("Preparing install image...")
    xterm_title("Preparing install image")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
        image_dir = project.image_dir(clean=True)
        
        run('pisi --yes-all -D"%s" ar pisilinux-install %s --ignore-check' % (image_dir, repo_dir + "/pisi-index.xml.bz2"))

        if project.type == "install":
            if project.all_install_image_packages:
                install_image_packages = project.all_install_image_packages
            else:
                install_image_packages = repo.full_deps("yali")
            run('pisi --yes-all --ignore-comar --ignore-dep -D"%s" it %s' % (image_dir, " ".join(install_image_packages)))
            if project.plugin_package:
                run('pisi --yes-all --ignore-comar -D"%s" it %s' % (image_dir, project.plugin_package))
        else:
            install_packages(project)

        try:
            run('/bin/mount --bind /proc %s/proc' % image_dir)
            run('/bin/mount --bind /sys %s/sys' % image_dir)
            run('/bin/mount --bind /dev %s/dev' % image_dir)
            run('/bin/mount --bind /dev/pts %s/dev/pts' % image_dir)
            
            # comar and pisi config
            chroot_comar(image_dir)
            
            # Diagnostics before pisi
            print("DEBUG: Checking socket inside chroot...")
            run('chroot "%s" ls -l /run/dbus/system_bus_socket' % image_dir, ignore_error=True)
            run('chroot "%s" ls -l /var/run/dbus/system_bus_socket' % image_dir, ignore_error=True)
            
            run('chroot "%s" /usr/bin/env DBUS_SYSTEM_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket /usr/bin/pisi configure-pending baselayout' % image_dir)
            
            # User management via DBus
            connectToDBus(image_dir)
            if bus:
                obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")
                # original logic for addUser...
                pass
        finally:
            run('umount -l %s/dev/pts' % image_dir, ignore_error=True)
            run('umount -l %s/dev' % image_dir, ignore_error=True)
            run('umount -l %s/proc' % image_dir, ignore_error=True)
            run('umount -l %s/sys' % image_dir, ignore_error=True)

        finished_path = os.path.join(project.work_dir, "finished.txt")
        with open(finished_path, 'w') as _file:
            _file.write("make-live")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: make_image() cancelled.")
        sys.exit(1)
