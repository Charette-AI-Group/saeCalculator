# PyInstaller build configuration — single-file windowed app.
# Build with: python -m PyInstaller saeCalculator.spec --noconfirm
# Output: dist/saeCalculator.exe (Windows) or dist/saeCalculator.app (macOS)

import sys

# Pillow (build extra) converts the icon to the platform format at build time.
appIcon = (
    "src/saeCalculator/resources/icon.png"
    if sys.platform == "darwin"
    else "src/saeCalculator/resources/icon.ico"
)

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
    icon=appIcon,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        name="saeCalculator.app",
        icon=appIcon,
        bundle_identifier="com.charette-ai-group.saeCalculator",
        info_plist={
            "NSHighResolutionCapable": True,
        },
    )
