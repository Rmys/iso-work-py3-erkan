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

# Qt
import os
import locale
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale

# Main form
from app.gui.main import MainWindow


def gui(args):
    # If no style is specified, use breeze as default
    if not any(arg.startswith("-style") for arg in args):
        args.append("-style")
        args.append("breeze")

    # Create applicatin
    app = QApplication(args)

    # Setup translations
    translator_code = QTranslator()
    translator_ui = QTranslator()
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    # Get system locale
    system_locale = QLocale.system().name()  # e.g., 'tr_TR'
    
    # Try to load translation files
    qm_code = os.path.join(project_root, 'locale', system_locale, 'LC_MESSAGES', 'pisiman.qm')
    qm_ui = os.path.join(project_root, 'locale', system_locale, 'LC_MESSAGES', 'pisiman_ui.qm')
    
    loaded = []
    if os.path.exists(qm_code) and translator_code.load(qm_code):
        app.installTranslator(translator_code)
        loaded.append("code")
    
    if os.path.exists(qm_ui) and translator_ui.load(qm_ui):
        app.installTranslator(translator_ui)
        loaded.append("UI")
    
    if loaded:
        print(f"Loaded translations ({system_locale}): {', '.join(loaded)}")
    else:
        print(f"No translations found for {system_locale}")

    # Load and apply modern style
    try:
        qss_path = os.path.join(os.path.dirname(__file__), "ui", "style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Style loading error: {e}")

    # Show main window
    mainWindow = MainWindow(args)
    mainWindow.show()

    app.setActiveWindow(mainWindow)

    # Close application if there's no window
    app.lastWindowClosed.connect(app.quit)

    # Go go go!
    app.exec()
