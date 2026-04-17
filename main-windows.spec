# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

project_root = os.path.abspath(".")

import sys
sys.path.insert(0, project_root)

datas = []
datas += collect_data_files("assets")
datas += collect_data_files("l10n")

a = Analysis(
    ['src/main.py'],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=collect_submodules('src'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Tutel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='assets/icons/tutel.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Tutel'
)
