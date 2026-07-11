# Session handoff — 2026-07-11 (laptop, travelling)

Context transfer between machines: Claude Code sessions and memory do not
sync, so this file carries the state. Read it at the start of the next
session on the desktop, then update or delete it once absorbed.

## What was done (all pushed to main)

- `c3a8bdf` — GitHub Actions workflow (`.github/workflows/build.yml`):
  every push builds `saeCalculator.exe` (windows-latest) and
  `saeCalculator.app` (macos-latest, Apple Silicon). Manual runs via the
  Actions tab. Made `saeCalculator.spec` platform-aware: BUNDLE section for
  a proper `.app` on macOS, icon.png/icon.ico picked per platform.
- `994a7da` — bumped actions to checkout@v7, setup-python@v6,
  upload-artifact@v7 (cleared Node 20 deprecation warnings).
- `49968a6` — README section "Automated builds (Windows + macOS)":
  artifact download, double-zip, Gatekeeper / `xattr -cr` instructions.
- `fa56fba` — `paths-ignore: **.md` so Markdown-only pushes skip builds.

Both CI jobs verified green twice (macOS ~47s, Windows ~1m39s).

## Pending / next steps

1. **macOS build untested on real hardware.** François planned to test the
   `.app` on an Apple Silicon Mac on 2026-07-11. If it failed, the fix is
   likely in `saeCalculator.spec` (BUNDLE section) — get the exact error,
   or run `./saeCalculator.app/Contents/MacOS/saeCalculator` from Terminal
   for output.
2. **Android was discussed, decision pending.** Options laid out:
   (a) `pyside6-android-deploy` on a GitHub Actions Linux runner — keeps
   the PySide6 stack, but the tool is a technical preview and the desktop
   UI needs a touch/portrait redesign; (b) recommended alternative: a PWA
   (single HTML page, engine ported to JS, hosted on GitHub Pages) — works
   on Android + iPhone with no store or signing; (c) Kivy/BeeWare — not
   favoured. The services/models layers are pure Python and port unchanged
   either way. François will choose the direction from the desktop.
3. Offered but not requested: a release job attaching binaries to GitHub
   Releases on version tags (artifacts expire after 90 days).
