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

        def addButton(self, text, role) -> object:
            return object()

        def clickedButton(self) -> None:
            return None

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


def testMarkDonatedHidesButtonAndPersists(qtbot, monkeypatch) -> None:
    from PySide6.QtCore import QSettings

    from saeCalculator import appConfig
    from saeCalculator.ui import mainWindow as mainWindowModule

    monkeypatch.setattr(
        mainWindowModule.QMessageBox, "information", staticmethod(lambda *args: None)
    )
    firstWindow = MainWindow()
    qtbot.addWidget(firstWindow)
    originallyDonated = firstWindow.donated

    try:
        firstWindow.markDonated()
        assert firstWindow.donated
        assert not firstWindow.calculatorWidget.donateButton.isVisible()

        secondWindow = MainWindow()
        qtbot.addWidget(secondWindow)
        assert secondWindow.donated
        assert secondWindow.calculatorWidget.donateButton.isHidden()
    finally:
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        settings.setValue("support/donated", originallyDonated)


def testDonateClickArmsReturnPrompt(qtbot, monkeypatch) -> None:
    from saeCalculator.ui import calculatorWidget as calculatorWidgetModule

    monkeypatch.setattr(
        calculatorWidgetModule.QDesktopServices, "openUrl", staticmethod(lambda url: True)
    )
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    assert not mainWindow.donatePromptPending

    qtbot.mouseClick(mainWindow.calculatorWidget.donateButton, Qt.MouseButton.LeftButton)
    assert mainWindow.donatePromptPending


def testDonationConfirmationYesMarksDonated(qtbot, monkeypatch) -> None:
    from PySide6.QtCore import QSettings

    from saeCalculator import appConfig
    from saeCalculator.ui import mainWindow as mainWindowModule

    monkeypatch.setattr(
        mainWindowModule.QMessageBox,
        "question",
        staticmethod(lambda *args: mainWindowModule.QMessageBox.StandardButton.Yes),
    )
    monkeypatch.setattr(
        mainWindowModule.QMessageBox, "information", staticmethod(lambda *args: None)
    )
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    originallyDonated = mainWindow.donated

    try:
        mainWindow.askDonationConfirmation()
        assert mainWindow.donated
        assert mainWindow.calculatorWidget.donateButton.isHidden()
    finally:
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        settings.setValue("support/donated", originallyDonated)


def testAboutTextContents(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)

    aboutText = mainWindow.buildAboutText()
    assert "SAE Fractional Calculator" in aboutText
    assert "Version 1.1.0" in aboutText
    assert "Editor: Francois Charette" in aboutText
    assert "AI Agent: Claude - Fable 5" in aboutText
    assert "Charette AI Group, LLC" in aboutText
