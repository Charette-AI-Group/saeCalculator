"""Application configuration — paths, defaults, and metadata."""

from __future__ import annotations

from pathlib import Path

appName = "SAE Fractional Calculator"
appVersion = "1.1.0"
organizationName = "Charette AI Group"

# Help > About contents
editorName = "Francois Charette"
aiAgentName = "Claude - Fable 5"
copyrightHolder = "Charette AI Group, LLC"

projectRoot = Path(__file__).resolve().parents[2]
resourcesDir = Path(__file__).resolve().parent / "resources"
iconPngPath = resourcesDir / "icon.png"
iconIcoPath = resourcesDir / "icon.ico"
companyMarkPaths = {
    "light": resourcesDir / "companyMarkLight.png",
    "dark": resourcesDir / "companyMarkDark.png",
}

# Distinct taskbar identity on Windows (otherwise the Python icon shows).
appUserModelId = "CharetteAIGroup.saeCalculator"

donateUrl = "https://www.paypal.com/donate/?hosted_button_id=FEM4WLD7LHY36"
windowTitle = appName
# Phone-like portrait proportions to match the keypad design.
defaultWindowWidth = 340
defaultWindowHeight = 620
