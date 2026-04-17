#!/bin/bash
set -e

APPDIR=AppDir

# Cleaning
rm -rf $APPDIR
mkdir -p $APPDIR/usr/bin
mkdir -p $APPDIR/usr/lib

# Copies the PyInstaller build in APPDIR
cp -r dist/Tutel/* $APPDIR/usr/bin/

# Copies the assets
cp -r assets $APPDIR/usr/bin/ || true
cp -r l10n $APPDIR/usr/bin/ || true

# Copies the Linux-specific files
cp linux/Tutel.desktop $APPDIR/
cp linux/Tutel.png $APPDIR/

# Makes the app executable
chmod +x $APPDIR/usr/bin/Tutel

# Creates the AppImage
appimagetool $APPDIR Tutel.AppImage
