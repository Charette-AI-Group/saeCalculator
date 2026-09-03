# PyInstaller build configuration — windowed app, one file or one folder.
#
#     python -m PyInstaller saeCalculator.spec --noconfirm
#         -> dist/saeCalculator.exe (Windows), dist/saeCalculator.app (macOS)
#
# With SAECALCULATOR_ONEDIR=1 in the environment it builds a folder bundle:
#
#         -> dist/saeCalculator/saeCalculator.exe
#
# That is what the Windows installer packages. A one-file build unpacks itself
# to a temp folder on every launch, which is a fair price for a download you
# hand somebody, and the wrong one for an application they installed.

import os
import sys

# Pillow (build extra) converts the icon to the platform format at build time.
appIcon = (
    "src/saeCalculator/resources/icon.png"
    if sys.platform == "darwin"
    else "src/saeCalculator/resources/icon.ico"
)

oneDir = os.environ.get("SAECALCULATOR_ONEDIR") == "1"

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

exeArguments = {
    "name": "saeCalculator",
    "debug": False,
    "bootloader_ignore_signals": False,
    "strip": False,
    "upx": False,
    "upx_exclude": [],
    "console": False,
    "icon": appIcon,
    "disable_windowed_traceback": False,
    "argv_emulation": False,
    "target_arch": None,
    "codesign_identity": None,
    "entitlements_file": None,
}

if oneDir:
    exe = EXE(pyz, a.scripts, [], exclude_binaries=True, **exeArguments)
    bundleTarget = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name="saeCalculator",
    )
else:
    exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], runtime_tmpdir=None, **exeArguments)
    bundleTarget = exe

if sys.platform == "darwin":
    app = BUNDLE(
        bundleTarget,
        name="saeCalculator.app",
        icon=appIcon,
        bundle_identifier="com.charette-ai-group.saeCalculator",
        info_plist={
            "NSHighResolutionCapable": True,
        },
    )
