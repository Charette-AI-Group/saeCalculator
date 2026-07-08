# PyInstaller build configuration — single-file windowed exe.
# Build with: python -m PyInstaller saeCalculator.spec --noconfirm
# Output: dist/saeCalculator.exe

a = Analysis(
    ["src/saeCalculator/main.py"],
    pathex=["src"],
    binaries=[],
    datas=[("src/saeCalculator/resources", "saeCalculator/resources")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="saeCalculator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon="src/saeCalculator/resources/icon.ico",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
