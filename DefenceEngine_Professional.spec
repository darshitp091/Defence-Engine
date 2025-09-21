# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['defence_engine_pure_supabase.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'threading', 'hashlib', 'json', 'datetime', 'random', 'time', 'os', 'sys', 'argparse', 'pathlib', 'requests', 'jwt', 'secrets'],
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
    name='DefenceEngine_Professional',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
