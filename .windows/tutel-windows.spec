# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

spec_path = os.path.abspath(sys.argv[0])
spec_dir = os.path.dirname(spec_path)
project_root = os.path.abspath(os.path.join(spec_dir, '..'))

import sys
sys.path.insert(0, project_root)

def collect_folder(folder):
    result = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, project_root)
            result.append((full, rel))
    return result

datas = []
datas += collect_folder(os.path.join(project_root, "assets"))
datas += collect_folder(os.path.join(project_root, "l10n"))

a = Analysis(
    [os.path.join(project_root, 'src/main.py')],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=collect_submodules(os.path.join(project_root, 'src')),
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
    icon=os.path.join(project_root, 'assets', 'icons', 'tutel.ico'),
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
