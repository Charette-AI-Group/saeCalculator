"""Light and dark theme palettes and stylesheet builders for the UI."""

from __future__ import annotations

from string import Template

themeModes = ("light", "dark")
defaultThemeMode = "light"

lightColors = {
    "windowBackground": "#f4f3ef",
    "displayBackground": "#ffffff",
    "displayBorder": "#d5d3cb",
    "expressionText": "#8a887c",
    "displayText": "#1f1e1b",
    "buttonBackground": "#ffffff",
    "buttonText": "#1f1e1b",
    "buttonBorder": "#d5d3cb",
    "buttonPressed": "#e9e7e1",
    "operatorText": "#5f5e5a",
    "unitBorder": "#b9b7af",
    "clearText": "#a32d2d",
    "fractionBackground": "#e6f1fb",
    "fractionText": "#185fa5",
    "fractionBorder": "#b5d4f4",
    "fractionPressed": "#cfe3f6",
    "equalsBackground": "#2c2c2a",
    "equalsText": "#ffffff",
    "equalsPressed": "#444441",
    "menuBackground": "#f4f3ef",
    "menuText": "#1f1e1b",
    "menuSelected": "#e2e0da",
    "switchTrackOff": "#b9b7af",
    "switchTrackOn": "#185fa5",
}

darkColors = {
    "windowBackground": "#22211f",
    "displayBackground": "#2c2b29",
    "displayBorder": "#454440",
    "expressionText": "#98968a",
    "displayText": "#f0eee8",
    "buttonBackground": "#32312e",
    "buttonText": "#f0eee8",
    "buttonBorder": "#454440",
    "buttonPressed": "#454440",
    "operatorText": "#b4b2a9",
    "unitBorder": "#5f5e5a",
    "clearText": "#f09595",
    "fractionBackground": "#0c344f",
    "fractionText": "#85b7eb",
    "fractionBorder": "#185fa5",
    "fractionPressed": "#10456a",
    "equalsBackground": "#e9e7e1",
    "equalsText": "#1f1e1b",
    "equalsPressed": "#cfcdc5",
    "menuBackground": "#22211f",
    "menuText": "#f0eee8",
    "menuSelected": "#3a3936",
    "switchTrackOff": "#5f5e5a",
    "switchTrackOn": "#378add",
}

themeColors = {"light": lightColors, "dark": darkColors}

calculatorTemplate = """
CalculatorWidget { background: $windowBackground; }
#displayFrame {
    background: $displayBackground;
    border: 1px solid $displayBorder;
    border-radius: 10px;
}
#expressionLabel { color: $expressionText; }
#currentLabel { color: $displayText; }
#themeIconLight, #themeIconDark { color: $operatorText; font-size: 14px; }
QPushButton {
    background: $buttonBackground;
    color: $buttonText;
    border: 1px solid $buttonBorder;
    border-radius: 10px;
    min-height: 52px;
    font-size: 21px;
}
QPushButton:pressed { background: $buttonPressed; }
QPushButton[keyClass="operator"] { color: $operatorText; font-size: 23px; }
QPushButton[keyClass="unit"] {
    min-height: 44px; font-size: 17px; font-weight: 600; border-color: $unitBorder;
}
QPushButton[keyClass="clear"] {
    min-height: 44px; font-size: 17px; font-weight: 600; color: $clearText;
}
QPushButton[keyClass="fraction"] {
    min-height: 42px; font-size: 17px;
    background: $fractionBackground; color: $fractionText; border-color: $fractionBorder;
}
QPushButton[keyClass="fraction"]:pressed { background: $fractionPressed; }
QPushButton[keyClass="company"] {
    background: transparent; border: none; min-height: 0px; padding: 0; border-radius: 8px;
}
QPushButton[keyClass="company"]:hover { background: $buttonPressed; }
QPushButton[keyClass="equals"] {
    background: $equalsBackground; color: $equalsText; border-color: $equalsBackground;
    font-weight: 600; font-size: 27px;
}
QPushButton[keyClass="equals"]:pressed { background: $equalsPressed; }
"""

windowTemplate = """
QMainWindow { background: $windowBackground; }
"""


def calculatorStyleSheet(mode: str) -> str:
    return Template(calculatorTemplate).substitute(themeColors[mode])


def windowStyleSheet(mode: str) -> str:
    return Template(windowTemplate).substitute(themeColors[mode])
