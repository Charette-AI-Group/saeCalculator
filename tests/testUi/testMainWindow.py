"""Smoke tests for the main window."""

from __future__ import annotations

from PySide6.QtCore import Qt

from saeCalculator.ui.calculatorWidget import CalculatorWidget
from saeCalculator.ui.mainWindow import MainWindow


def testMainWindowOpens(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    mainWindow.show()

    assert mainWindow.isVisible()
    assert mainWindow.windowTitle() == "SAE Fractional Calculator"
    assert not mainWindow.windowIcon().isNull()


def testCalculatorIsCentralWidget(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)

    assert isinstance(mainWindow.centralWidget(), CalculatorWidget)
    assert mainWindow.centralWidget() is mainWindow.calculatorWidget


def testNoMenuBarShown(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)

    assert not mainWindow.menuBar().actions()


def testCompanyButtonOpensAbout(qtbot, monkeypatch) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    mainWindow.show()

    execCalls = []

    class FakeAboutBox:
        def exec(self) -> None:
            execCalls.append(True)

    monkeypatch.setattr(mainWindow, "buildAboutBox", lambda: FakeAboutBox())
    companyButton = mainWindow.calculatorWidget.companyButton
    assert not companyButton.icon().isNull()

    qtbot.mouseClick(companyButton, Qt.MouseButton.LeftButton)
    assert execCalls == [True]


def testThemeSwitching(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    originalMode = mainWindow.currentThemeMode

    themeToggle = mainWindow.calculatorWidget.themeToggle
    try:
        themeToggle.setChecked(True)
        assert mainWindow.currentThemeMode == "dark"
        assert "#22211f" in mainWindow.styleSheet()
        assert "#22211f" in mainWindow.calculatorWidget.styleSheet()

        themeToggle.setChecked(False)
        assert mainWindow.currentThemeMode == "light"
        assert not themeToggle.isChecked()
        assert "#f4f3ef" in mainWindow.calculatorWidget.styleSheet()
    finally:
        # Theme choice persists via QSettings; restore the user's setting.
        mainWindow.onThemeSelected(originalMode)


def testThemeModePersistsAcrossWindows(qtbot) -> None:
    firstWindow = MainWindow()
    qtbot.addWidget(firstWindow)
    originalMode = firstWindow.currentThemeMode

    try:
        firstWindow.onThemeSelected("dark")
        secondWindow = MainWindow()
        qtbot.addWidget(secondWindow)
        assert secondWindow.currentThemeMode == "dark"
    finally:
        firstWindow.onThemeSelected(originalMode)


def testAboutTextContents(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)

    aboutText = mainWindow.buildAboutText()
    assert "SAE Fractional Calculator" in aboutText
    assert "Version 1.0.0" in aboutText
    assert "Editor: Francois Charette" in aboutText
    assert "AI Agent: Claude - Fable 5" in aboutText
    assert "Charette AI Group, LLC" in aboutText
