"""Application configuration — paths, defaults, and metadata."""

from __future__ import annotations

from pathlib import Path

appName = "SAE Fractional Calculator"
appVersion = "0.1.0"
organizationName = "Charette AI Group"

projectRoot = Path(__file__).resolve().parents[2]
resourcesDir = Path(__file__).resolve().parent / "resources"
windowTitle = appName
defaultWindowWidth = 800
defaultWindowHeight = 600
