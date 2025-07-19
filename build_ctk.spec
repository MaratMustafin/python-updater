# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Анализ для CustomTkinter версии
a_ctk = Analysis(
    ['main_ctk.py'],
    pathex=[],
    binaries=[],
    datas=[('translations.json', '.'), ('README.md', '.')],
    hiddenimports=[
        'customtkinter',
        'darkdetect',
        'PIL._tkinter_finder'
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

pyz_ctk = PYZ(a_ctk.pure, a_ctk.zipped_data, cipher=block_cipher)

exe_ctk = EXE(
    pyz_ctk,
    a_ctk.scripts,
    a_ctk.binaries,
    a_ctk.zipfiles,
    a_ctk.datas,
    [],
    name='PythonUpdater_CTK',
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
app_ctk = BUNDLE(
    exe_ctk,
    name='PythonUpdater_CTK.app',
    icon=None,
    bundle_identifier='com.yourcompany.pythonupdater.ctk',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.13.0',
    },
)
