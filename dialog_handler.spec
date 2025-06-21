# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['dialog_handler.py'],
    pathex=[],
    binaries=[],
    datas=[('imgs', 'imgs'), ('utils.py', '.')],
    hiddenimports=['cv2', 'pyautogui', 'numpy', 'PIL', 'PIL._tkinter_finder', 'tkinter', 'pyscreeze', 'pytweening', 'mouseinfo', 'keyboard', 'pygetwindow', 'pyrect'],
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
    name='dialog_handler',
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
