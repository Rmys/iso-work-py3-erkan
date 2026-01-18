#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
from .utility import run

def setup_live_kdm(project):
    image_dir = project.image_dir()
    kdmrc_path = os.path.join(image_dir, "etc/X11/kdm/kdmrc")
    if os.path.exists(kdmrc_path):
        lines = []
        with open(kdmrc_path, "r") as f:
            for line in f.readlines():
                if line.startswith("#AutoLoginEnable"):
                    lines.append("AutoLoginEnable=true\n")
                elif line.startswith("#AutoLoginUser"):
                    lines.append("AutoLoginUser=pisi\n")
                elif line.startswith("#ServerTimeout="):
                    lines.append("ServerTimeout=60\n")
                else:
                    lines.append(line)
        with open(kdmrc_path, "w") as f:
            f.write("".join(lines))
    else:
        print("*** %s doesn't exist, setup_live_kdm() returned" % kdmrc_path)

def setup_live_sddm(project):
    image_dir = project.image_dir()
    shutil.copy("./data/sddm/sddm.conf.d/sddm.conf", "{}/usr/lib/sddm/sddm.conf.d/".format(image_dir))
    shutil.copy("./data/etc/timezone", "{}/etc/".format(image_dir))

def setup_live_lxdm(project):
    image_dir = project.image_dir()
    lxdmconf_path = os.path.join(image_dir, "etc/lxdm/lxdm.conf")
    if os.path.exists(lxdmconf_path):
        lines = []
        with open(lxdmconf_path, "r") as f:
            for line in f.readlines():
                if line.startswith("# autologin=") or line.startswith("autologin="):
                    lines.append("autologin=pisi\n session=/usr/bin/startkde\n")
                elif line.startswith("session="):
                    if os.path.exists("%s/usr/bin/mate-session" % image_dir):
                        lines.append("session=/usr/bin/mate-session\n")
                    elif os.path.exists("%s/usr/bin/startxfce4" % image_dir):
                        lines.append("session=/usr/bin/startxfce4\n")
                    elif os.path.exists("%s/usr/bin/startlxqt" % image_dir):
                        lines.append("session=/usr/bin/startlxqt\n")
                    elif os.path.exists("%s/usr/bin/startlxde" % image_dir):
                        lines.append("session=/usr/bin/startlxde\n")
                else:
                    lines.append(line)
        with open(lxdmconf_path, "w") as f:
            f.write("".join(lines))
    else:
        print("*** {} doesn't exist, setup_live_lxdm() returned".format(lxdmconf_path))

def setup_live_lightdm(project):
    image_dir = project.image_dir()
    lxdmconf_path = os.path.join(image_dir, "etc/lightdm/lightdm.conf")
    if os.path.exists(lxdmconf_path):
        lines = []
        with open(lxdmconf_path, "r") as f:
            for line in f.readlines():
                if line.startswith("#autologin-user=") or line.startswith("autologin-user="):
                    lines.append("autologin-user=pisi\n")
                elif line.startswith("#autologin-session="):
                    sessions = os.listdir("%s/usr/share/xsessions" % image_dir)
                    session = sessions[0].split(".")[0]
                    lines.append("autologin-session=%s\n" % session)
                else:
                    lines.append(line)
        with open(lxdmconf_path, "w") as f:
            f.write("".join(lines))
    else:
        print("*** {} doesn't exist, setup_live_lxdm() returned".format(lxdmconf_path))

def setup_live_gdm(project):
    image_dir = project.image_dir()
    gdmconf_path = os.path.join(image_dir, "etc/gdm/custom.conf")
    if os.path.exists(gdmconf_path):
        lines = []
        with open(gdmconf_path, "r") as f:
            for line in f.readlines():
                if line.startswith("[daemon]"):
                    lines.append(line)
                    lines.append("AutomaticLoginEnable=True\n")
                    lines.append("AutomaticLogin=pisi\n")
                else:
                    lines.append(line)
        with open(gdmconf_path, "w") as f:
            f.write("".join(lines))
    else:
        print("*** {} doesn't exist, setup_live_gdm() returned".format(gdmconf_path))

def setup_live_dm(project, dm):
    if dm == "sddm":
        setup_live_sddm(project)
    elif dm == "lxdm":
        setup_live_lxdm(project)
    elif dm == "lightdm":
        setup_live_lightdm(project)
    elif dm == "gdm":
        setup_live_gdm(project)

def setup_live_policykit_conf(project):
    policykit_conf_tmpl = """[Live CD Rules]
Identity=unix-user:pisi
Action=*
ResultAny=yes
ResultInactive=yes
ResultActive=yes
"""
    image_dir = project.image_dir()
    os.makedirs(os.path.join(image_dir, "etc/polkit-1/localauthority/90-mandatory.d"), 0o644, exist_ok=True)
    dest = os.path.join(image_dir, "etc/polkit-1/localauthority/90-mandatory.d/livecd.pkla")
    with open(dest, "w") as f:
        f.write(policykit_conf_tmpl)
