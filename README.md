# SAE Fractional Calculator

Calculator for fractional computation needed during DIY projects (PySide6).

Try it in the browser (JS port of the same calculator, in `docs/`):
https://saecalculator.com — installable on phones via Add to Home Screen.

Lengths are entered in yards, feet, inches, and fractions of an inch, and all
math is done in exact integer counts of 1/32 inch. Results are always shown
in feet-inches with a reduced fraction (e.g. `4' 0-1/4"`).

## Using the calculator

Type a number, then press the key that says what it is:

| Key | Meaning | Example |
|-----|---------|---------|
| `yd` `ft` `in` | Commits the pending number as that unit | `1` `ft` `6` `in` |
| `/2` `/4` `/8` `/16` `/32` | Commits the pending number as a numerator | `1` `/2` = 1/2" |
| `+` `−` `×` `÷` | Operators (× and ÷ take a plain-number right operand) | |
| `=` | Evaluates; result shown in feet-inches | |
| `C` / `⌫` | Clear all / erase last digit | |

Example: `1' 6-1/2" + 2' 5-3/4"` is typed as
`1` `ft` `6` `in` `1` `/2` `+` `2` `ft` `5` `in` `3` `/4` `=` → `4' 0-1/4"`.

Keyboard entry mirrors the keypad: digits, `.`, `+ - * /`, Enter or `=`,
Backspace, Esc to clear, and `y` / `f` (or `'`) / `i` (or `"`) for units.

## One-time setup

```powershell
cd W:\projects\26saeCalculator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Daily workflow

```powershell
cd W:\projects\26saeCalculator
.\.venv\Scripts\Activate.ps1
saeCalculator
```

Or without the script entry point:

```powershell
python -m saeCalculator.main
```

## Build a standalone exe

One-time: install the build tooling into the venv:

```powershell
pip install -e ".[build]"
```

The app icon lives in `src/saeCalculator/resources/` (`icon.png` for the
window, `icon.ico` for the exe). To change it, edit and rerun
`tools/generateIcon.py`.

Then build (takes a minute or two):

```powershell
python -m PyInstaller saeCalculator.spec --noconfirm
```

The result is a single shareable file, `dist\saeCalculator.exe` (~45 MB — it
bundles Python and Qt, so it runs on machines with neither installed). First
launch is a little slow because the exe unpacks itself to a temp folder.

## Build the Windows installer

```powershell
python tools/buildInstaller.py
```

That builds a folder bundle (`dist\saeCalculator\`) and compiles it into
`dist\saeCalculatorSetup-<version>.exe` — the installed app starts instantly
because nothing has to be unpacked at launch. The installer is per-user: no
administrator rights, no UAC prompt, Start menu and optional desktop
shortcuts, and an entry in Add/Remove Programs. Uninstalling removes the
application but keeps the theme and donation settings under `HKCU`, so a
reinstall picks up where you left off.

Needs Inno Setup 6 (`winget install JRSoftware.InnoSetup`). The version and
the installer name come from `appConfig.appVersion`, never from the `.iss`.

Notes for sharing:
- Windows SmartScreen may warn on an unsigned exe downloaded from the
  internet ("More info" > "Run anyway"). Sharing over a LAN or USB usually
  avoids this.
- The theme preference is stored per user in the registry, so it persists
  for whoever runs it.

## Automated builds (Windows + macOS)

Every push to GitHub builds the app for both platforms via GitHub Actions
(`.github/workflows/build.yml`); a build can also be started manually from
the repo's Actions tab ("Run workflow"). Download from the run page, under
"Artifacts":

- `saeCalculator-windows` — `saeCalculatorSetup-<version>.exe` (installer)
  and `saeCalculator.exe` (single-file portable build)
- `saeCalculator-macos-appleSilicon` — `saeCalculator.app` for Apple Silicon
  Macs (M1 or newer, ~2021+); it does not run on Intel Macs

Artifacts expire after 90 days; rerun the workflow to rebuild.

Notes for the macOS app:
- The artifact download unzips twice: GitHub wraps it in a zip that contains
  `saeCalculator-macos.zip`, which contains `saeCalculator.app`.
- The app is unsigned, so on first launch right-click it > "Open" (don't
  double-click). If macOS instead claims the app "is damaged", it isn't —
  that's Gatekeeper quarantining an unsigned download. Clear it in Terminal
  with `xattr -cr path/to/saeCalculator.app`, then launch normally. Proper
  signing/notarization needs an Apple Developer account; skip it for
  personal use.

To publish a release, push a version tag. The workflow attaches the builds to
a GitHub Release (release assets never expire) and uses the tag's own message
as the release notes. Bump `appConfig.appVersion` first, along with
`pyproject.toml` and the version the About-box test expects: the installer
name comes from it, and the workflow does not check that the tag matches.

```powershell
git tag -a v1.3.0 -m "What changed in this release" ; git push origin v1.3.0
```

`git tag` deletes lines starting with `#` by default, so if the notes use
Markdown headings, write them to a file and tag with `--cleanup=whitespace`
instead:

```powershell
git tag -a v1.3.0 --cleanup=whitespace -F notes.md ; git push origin v1.3.0
```

## Tests and lint

```powershell
pytest
ruff check src tests
```

## Structure

| Layer | Folder | Purpose |
|-------|--------|---------|
| Entry | `src/saeCalculator/main.py` | Start `QApplication`, show main window |
| Config | `src/saeCalculator/appConfig.py` | Paths, defaults, app metadata |
| UI | `src/saeCalculator/ui/` | Widgets and dialogs only |
| Services | `src/saeCalculator/services/` | Business logic (no Qt widgets) |
| Models | `src/saeCalculator/models/` | Plain Python data types |

See `AGENTS.md` for architecture and naming conventions (for you and AI agents).

## License

[MIT](LICENSE) — free to use, modify and redistribute, including commercially, provided the copyright notice is kept. The software comes with no warranty.

---
*Created from the Qt App Template.*
