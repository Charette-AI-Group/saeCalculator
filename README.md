# SAE Fractional Calculator

Calculator for fractional computation needed during DIY projects (PySide6)

## One-time setup

```powershell
cd W:\projects\saeCalculator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Daily workflow

```powershell
cd W:\projects\saeCalculator
.\.venv\Scripts\Activate.ps1
saeCalculator
```

Or without the script entry point:

```powershell
python -m saeCalculator.main
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

---
*Created from the Qt App Template.*
