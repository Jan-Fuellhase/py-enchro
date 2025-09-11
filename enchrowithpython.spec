# -*- mode: python ; coding: utf-8 -*-
import os
block_cipher = None

# Pull in Kivy Windows dependency DLLs
from kivy_deps import sdl2, glew, angle

a = Analysis(
    ['enchrowithpython.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'win32timezone',
        'win32api',
        'win32con',
        'pywintypes',
        'pkg_resources.extern',
        'pkg_resources.py2_warn',
        'kivy.deps.sdl2',
        'kivy.deps.glew',
        'kivy.deps.angle'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + angle.dep_bins)],
    name='enchrowithpython',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # windowed app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)