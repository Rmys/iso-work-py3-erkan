#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import hashlib
from .utility import run, xterm_title

def make_repos(project):
    print("Preparing image repo...")
    xterm_title("Preparing repo")

    try:
        repo = project.get_repo(update_repo=True)
        repo_dir = project.image_repo_dir(clean=True)
        if project.type == "install":
            imagedeps = project.all_install_image_packages or repo.full_deps("yali")
            xterm_title("Preparing image repo for installation")
        else:
            if 'Calamares' in project.all_packages:
                imagedeps = project.all_packages
            else:
                imagedeps = project.all_install_image_packages
            xterm_title("Preparing image repo for live")

        repo.make_local_repo(repo_dir, imagedeps)

        xterm_title("Preparing installation repo")
        print("Preparing installation repository...")

        repo_dir = project.install_repo_dir(clean=True)
        if project.package_collections:
            all_packages = []
            for collection in project.package_collections:
                all_packages.extend(collection.packages.allPackages)
                repo.make_local_repo(repo_dir, collection.packages.allPackages, collection._id)

            repo.make_local_repo(repo_dir, all_packages)
            repo.make_collection_index(repo_dir, project.package_collections, project.default_language)
            print("Preparing collections project file")
        else:
            repo.make_local_repo(repo_dir, project.all_packages)

        finished_path = os.path.join(project.work_dir, "finished.txt")
        with open(finished_path, 'w') as _file:
            _file.write("make-repo")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: make_repo() cancelled.")
        sys.exit(1)

def check_file(repo_dir, name, _hash):
    path = os.path.join(repo_dir, name)
    if not os.path.exists(path):
        print("\nPackage missing: %s" % path)
        return
    with open(path, "rb") as f:
        data = f.read()
    cur_hash = hashlib.sha1(data).hexdigest()
    if cur_hash != _hash:
        print("\nWrong hash: %s" % path)
        return False
    return True

def check_repo_files(project):
    print("Checking image repo...")
    xterm_title("Checking image repo")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
        if project.type == "install":
            imagedeps = project.all_install_image_packages or repo.full_deps("yali")
        else:
            if 'Calamares' in project.all_packages:
                imagedeps = project.all_packages
            else:
                imagedeps = project.all_install_image_packages

        missing_pakc = []
        i = 0
        for name in imagedeps:
            i += 1
            sys.stdout.write("\r%-70.70s" % ("Checking %d of %s packages" % (i, len(imagedeps))))
            sys.stdout.flush()
            pak = repo.packages[name]
            if not check_file(repo_dir, pak.uri, pak.sha1sum):
                missing_pakc.append(name)
        sys.stdout.write("\n")

        repo_dir = project.install_repo_dir()
        i = 0
        for name in project.all_packages:
            i += 1
            sys.stdout.write("\r%-70.70s" % ("Checking %d of %s packages" % (i, len(project.all_packages))))
            sys.stdout.flush()
            pak = repo.packages[name]
            if not check_file(repo_dir, pak.uri, pak.sha1sum):
                if name not in missing_pakc:
                    missing_pakc.append(name)

        sys.stdout.write("\n")

        if len(missing_pakc) > 0:
            missing = os.path.join(project.work_dir, "missing.txt")
            with open(missing, 'w') as _file:
                _file.write("\n".join(missing_pakc))
            print("Some packages has wrong hash")
            sys.exit(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt: check_repo() cancelled.")
        sys.exit(1)
