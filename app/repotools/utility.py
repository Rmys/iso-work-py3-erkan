#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
import subprocess
import re

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def run(cmd, ignore_error=False):
    print(cmd)
    try:
        ret = subprocess.run(cmd, shell=True, check=not ignore_error)
        return ret.returncode
    except subprocess.CalledProcessError as e:
        print("%s returned %s" % (cmd, e.returncode))
        if not ignore_error:
            sys.exit(1)
        return e.returncode

def I18N_NOOP(x):
    return x

def size_fmt(size):
    parts = []
    if size == 0:
        return "0"
    while size > 0:
        parts.append("%03d" % (size % 1000))
        size //= 1000
    parts.reverse()
    tmp = ".".join(parts)
    return tmp.lstrip("0")

def xterm_title(message):
    """Set message as console window title."""
    if "TERM" in os.environ and sys.stderr.isatty():
        terminalType = os.environ["TERM"]
        for term in ["xterm", "Eterm", "aterm", "rxvt", "screen", "kterm", "rxvt-unicode"]:
            if terminalType.startswith(term):
                sys.stderr.write("\x1b]2;"+str(message)+"\x07")
                sys.stderr.flush()
                break

def wait_bus(unix_name, timeout=5, wait=0.1, stream=True):
    import socket
    import time
    if stream:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    while timeout > 0:
        try:
            sock.connect(unix_name)
            return True
        except:
            timeout -= wait
        time.sleep(wait)
    return False
