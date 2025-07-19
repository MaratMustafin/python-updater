# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_ctk.py'],
    pathex=[],
    binaries=[],
    datas=[('translations.json', '.'), ('README.md', '.')],
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
        'appdirs',
        'hashlib',
        'json',
        'pathlib',
        'threading',
        'logging'
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
    icon='icon.ico',
)

# Для macOS
app = BUNDLE(
    exe,
    name='PythonUpdater_CustomTkinter.app',
    icon='icon.icns',
    bundle_identifier='com.pythonupdater.customtkinter',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.15.0',
        'CFBundleDisplayName': 'Python Updater',
        'CFBundleName': 'Python Updater',
    },
)
