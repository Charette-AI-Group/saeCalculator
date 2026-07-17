"""Calculator display and keypad — replica of the approved phone mockup."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QKeyEvent
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from saeCalculator import appConfig
from saeCalculator.services.calculatorEngine import CalculatorEngine
from saeCalculator.ui import theme
from saeCalculator.ui.toggleSwitch import ToggleSwitch

# (label, key, keyClass) — keys are the engine's key strings.
unitRowKeys = [
    ("C", "C", "clear"),
    ("yd", "yd", "unit"),
    ("ft", "ft", "unit"),
    ("in", "in", "unit"),
]
fractionRowKeys = [(f"/{d}", f"f{d}", "fraction") for d in (2, 4, 8, 16, 32)]
mainGridKeys = [
    [("7", "7", "digit"), ("8", "8", "digit"), ("9", "9", "digit"), ("÷", "op/", "operator")],
    [("4", "4", "digit"), ("5", "5", "digit"), ("6", "6", "digit"), ("×", "op*", "operator")],
    [("1", "1", "digit"), ("2", "2", "digit"), ("3", "3", "digit"), ("−", "op-", "operator")],
    [("0", "0", "digit"), (".", ".", "digit"), ("⌫", "B", "digit"), ("+", "op+", "operator")],
]

keyboardShortcuts = {
    "+": "op+",
    "-": "op-",
    "*": "op*",
    "/": "op/",
    "=": "eq",
    "y": "yd",
    "f": "ft",
    "i": "in",
    "'": "ft",
    '"': "in",
}

class CalculatorWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.engine = CalculatorEngine()
        self.keyButtons: dict[str, QPushButton] = {}
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.buildUi()
        self.applyTheme(theme.defaultThemeMode)
        self.refreshDisplay()

    def applyTheme(self, mode: str) -> None:
        self.setStyleSheet(theme.calculatorStyleSheet(mode))
        colors = theme.themeColors[mode]
        self.themeToggle.setTrackColors(
            QColor(colors["switchTrackOff"]), QColor(colors["switchTrackOn"])
        )
        self.themeToggle.setChecked(mode == "dark")
        self.companyButton.setIcon(QIcon(str(appConfig.companyMarkPaths[mode])))

    def buildUi(self) -> None:
        rootLayout = QVBoxLayout(self)
        rootLayout.setContentsMargins(14, 14, 14, 14)
        rootLayout.setSpacing(8)

        # Stretch factors let the keypad fill all vertical space below the
        # display; buttons expand (see createButton), so no gap at the bottom.
        rootLayout.addLayout(self.buildThemeRow())
        rootLayout.addWidget(self.buildDisplay())
        rootLayout.addLayout(self.buildKeyRow(unitRowKeys), 1)
        rootLayout.addLayout(self.buildKeyRow(fractionRowKeys), 1)
        rootLayout.addLayout(self.buildMainGrid(), 6)

    def buildThemeRow(self) -> QHBoxLayout:
        lightIcon = QLabel("☀")
        lightIcon.setObjectName("themeIconLight")
        self.themeToggle = ToggleSwitch()
        self.themeToggle.setToolTip("Switch between light and dark mode")
        darkIcon = QLabel("☾")
        darkIcon.setObjectName("themeIconDark")

        self.companyButton = QPushButton()
        self.companyButton.setProperty("keyClass", "company")
        self.companyButton.setToolTip(f"About {appConfig.appName}")
        self.companyButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.companyButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.companyButton.setIconSize(QSize(26, 26))
        self.companyButton.setFixedSize(32, 32)

        themeRow = QHBoxLayout()
        themeRow.setSpacing(6)
        themeRow.addWidget(lightIcon)
        themeRow.addWidget(self.themeToggle)
        themeRow.addWidget(darkIcon)
        themeRow.addStretch()
        themeRow.addWidget(self.companyButton)
        return themeRow

    def buildDisplay(self) -> QFrame:
        displayFrame = QFrame()
        displayFrame.setObjectName("displayFrame")

        self.expressionLabel = QLabel("")
        self.expressionLabel.setObjectName("expressionLabel")
        self.expressionLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        expressionFont = QFont("Consolas", 9)
        expressionFont.setStyleHint(QFont.StyleHint.Monospace)
        self.expressionLabel.setFont(expressionFont)

        self.currentLabel = QLabel("")
        self.currentLabel.setObjectName("currentLabel")
        self.currentLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        currentFont = QFont("Consolas", 18, QFont.Weight.DemiBold)
        currentFont.setStyleHint(QFont.StyleHint.Monospace)
        self.currentLabel.setFont(currentFont)

        displayLayout = QVBoxLayout(displayFrame)
        displayLayout.setContentsMargins(12, 10, 12, 10)
        displayLayout.setSpacing(2)
        displayLayout.addWidget(self.expressionLabel)
        displayLayout.addWidget(self.currentLabel)
        return displayFrame

    def buildKeyRow(self, rowKeys: list[tuple[str, str, str]]) -> QGridLayout:
        rowLayout = QGridLayout()
        rowLayout.setSpacing(8)
        for column, (label, key, keyClass) in enumerate(rowKeys):
            rowLayout.addWidget(self.createButton(label, key, keyClass), 0, column)
        return rowLayout

    def buildMainGrid(self) -> QGridLayout:
        gridLayout = QGridLayout()
        gridLayout.setSpacing(8)
        for row, rowKeys in enumerate(mainGridKeys):
            for column, (label, key, keyClass) in enumerate(rowKeys):
                gridLayout.addWidget(self.createButton(label, key, keyClass), row, column)
        equalsButton = self.createButton("=", "eq", "equals")
        gridLayout.addWidget(equalsButton, len(mainGridKeys), 0, 1, 4)
        return gridLayout

    def createButton(self, label: str, key: str, keyClass: str) -> QPushButton:
        button = QPushButton(label)
        button.setProperty("keyClass", keyClass)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Buttons never take focus so typing always reaches keyPressEvent.
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.clicked.connect(lambda checked=False, k=key: self.pressKey(k))
        self.keyButtons[key] = button
        return button

    def pressKey(self, key: str) -> None:
        self.engine.press(key)
        self.refreshDisplay()

    def refreshDisplay(self) -> None:
        self.expressionLabel.setText(self.engine.expressionText)
        self.currentLabel.setText(self.engine.displayText)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = self.engineKeyFromEvent(event)
        if key is None:
            super().keyPressEvent(event)
            return
        self.pressKey(key)

    def engineKeyFromEvent(self, event: QKeyEvent) -> str | None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            return "eq"
        if event.key() == Qt.Key.Key_Backspace:
            return "B"
        if event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Delete):
            return "C"
        text = event.text()
        if text.isdigit() or text == ".":
            return text
        return keyboardShortcuts.get(text.lower())
