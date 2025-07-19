# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Анализ для DearPyGui версии
a_dpg = Analysis(
    ['main_dpg.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['dearpygui.dearpygui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz_dpg = PYZ(a_dpg.pure, a_dpg.zipped_data, cipher=block_cipher)

exe_dpg = EXE(
    pyz_dpg,
    a_dpg.scripts,
    a_dpg.binaries,
    a_dpg.zipfiles,
    a_dpg.datas,
    [],
    name='PythonUpdater_DPG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# Для macOS
app_dpg = BUNDLE(
    exe_dpg,
    name='PythonUpdater_DPG.app',
    icon=None,
    bundle_identifier='com.yourcompany.pythonupdater.dpg',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.13.0',
    },
)
