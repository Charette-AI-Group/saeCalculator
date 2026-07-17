"""Smoke tests for the main window."""

from __future__ import annotations

from saeCalculator.ui.calculatorWidget import CalculatorWidget
from saeCalculator.ui.mainWindow import MainWindow


def testMainWindowOpens(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    mainWindow.show()

    assert mainWindow.isVisible()
    assert mainWindow.windowTitle() == "SAE Fractional Calculator"
    assert mainWindow.statusBar().currentMessage() == "Ready"
    assert not mainWindow.windowIcon().isNull()


def testCalculatorIsCentralWidget(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)

    assert isinstance(mainWindow.centralWidget(), CalculatorWidget)
    assert mainWindow.centralWidget() is mainWindow.calculatorWidget


def testMenuBarStructure(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)

    menuTitles = [action.text() for action in mainWindow.menuBar().actions()]
    assert menuTitles == ["&Options", "&Help"]

    assert [a.text() for a in mainWindow.optionsMenu.actions()] == ["&Light Mode", "&Dark Mode"]
    assert [a.text() for a in mainWindow.helpMenu.actions()] == ["&About"]


def testThemeSwitching(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    originalMode = mainWindow.currentThemeMode

    try:
        mainWindow.darkModeAction.trigger()
        assert mainWindow.currentThemeMode == "dark"
        assert mainWindow.darkModeAction.isChecked()
        assert not mainWindow.lightModeAction.isChecked()
        assert "#22211f" in mainWindow.styleSheet()
        assert "#22211f" in mainWindow.calculatorWidget.styleSheet()

        mainWindow.lightModeAction.trigger()
        assert mainWindow.currentThemeMode == "light"
        assert mainWindow.lightModeAction.isChecked()
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


def testCopyrightShownInStatusBar(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)

    assert mainWindow.copyrightLabel.parent() is mainWindow.statusBar()
    assert "©" in mainWindow.copyrightLabel.text()
    assert "Charette AI Group, LLC" in mainWindow.copyrightLabel.text()
