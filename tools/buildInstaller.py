r"""Build the Windows installer: folder bundle first, then Inno Setup.

    .venv\Scripts\python.exe tools\buildInstaller.py

Produces dist\saeCalculatorSetup-<version>.exe. The version is read from the
application rather than typed into the .iss, so the installer, the About box
and the wheel cannot disagree about what this is - a person keeping three
files in step is the one thing here that is certain to drift.

Needs Inno Setup 6. On a GitHub Windows runner it is already there; locally,
winget install JRSoftware.InnoSetup puts it under LOCALAPPDATA rather than in
Program Files, so both are looked for.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

projectRoot = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(projectRoot / "src"))

specFile = projectRoot / "saeCalculator.spec"
scriptFile = projectRoot / "installer" / "saeCalculator.iss"
bundleDir = projectRoot / "dist" / "saeCalculator"
outputDir = projectRoot / "dist"
buildTimeoutSeconds = 900.0

compilerCandidates = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Inno Setup 6" / "ISCC.exe",
    Path(os.environ.get("ProgramFiles(x86)", "")) / "Inno Setup 6" / "ISCC.exe",
    Path(os.environ.get("ProgramFiles", "")) / "Inno Setup 6" / "ISCC.exe",
]


def findCompiler() -> Path | None:
    for candidate in compilerCandidates:
        if candidate.name and candidate.is_file():
            return candidate
    return None


def appVersion() -> str:
    from saeCalculator import appConfig

    return appConfig.appVersion


def run(command: list[str], environment: dict[str, str] | None = None) -> int:
    print(f"$ {subprocess.list2cmdline(command)}")
    completed = subprocess.run(
        command, cwd=projectRoot, env=environment, timeout=buildTimeoutSeconds
    )
    return completed.returncode


def buildBundle() -> int:
    # The installer packages the folder bundle, never the one-file exe: an
    # installed application should not unpack itself on every launch.
    environment = dict(os.environ, SAECALCULATOR_ONEDIR="1")
    command = [sys.executable, "-m", "PyInstaller", str(specFile), "--noconfirm"]
    return run(command, environment)


def main() -> int:
    if sys.platform != "win32":
        print("The installer is a Windows artifact; nothing to do here.")
        return 0

    compiler = findCompiler()
    if compiler is None:
        print("Inno Setup 6 was not found. Looked in:")
        for candidate in compilerCandidates:
            print(f"  {candidate}")
        print("\nInstall it with:  winget install JRSoftware.InnoSetup")
        return 1

    buildCode = buildBundle()
    if buildCode != 0:
        print(f"\nPyInstaller failed with code {buildCode}.")
        return buildCode
    if not (bundleDir / "saeCalculator.exe").is_file():
        print(f"\nPyInstaller reported success but {bundleDir} holds no exe.")
        return 1

    version = appVersion()
    compileCode = run([str(compiler), f"/DAppVersion={version}", str(scriptFile)])
    if compileCode != 0:
        print(f"\nInno Setup failed with code {compileCode}.")
        return compileCode

    installer = outputDir / f"saeCalculatorSetup-{version}.exe"
    if not installer.is_file():
        print(f"\nInno Setup reported success but {installer} is not there.")
        return 1
    print(f"\nInstaller: {installer}")
    print(f"Size     : {installer.stat().st_size / 1_000_000:.0f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
