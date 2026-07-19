"""Main application window."""

from __future__ import annotations

import datetime

from PySide6.QtCore import QEvent, QSettings, Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from saeCalculator import appConfig
from saeCalculator.ui import theme
from saeCalculator.ui.calculatorWidget import CalculatorWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.donatePromptPending = False
        self.donateWindowLeft = False
        self.setWindowTitle(appConfig.windowTitle)
        self.setWindowIcon(QIcon(str(appConfig.iconPngPath)))
        self.resize(appConfig.defaultWindowWidth, appConfig.defaultWindowHeight)

        self.calculatorWidget = CalculatorWidget()
        self.setCentralWidget(self.calculatorWidget)
        self.calculatorWidget.setFocus()

        self.applyTheme(self.loadThemeMode())
        self.calculatorWidget.themeToggle.toggled.connect(self.onThemeToggled)
        self.calculatorWidget.companyButton.clicked.connect(self.onHelpAbout)

        self.donated = self.loadDonated()
        self.calculatorWidget.donateButton.setVisible(not self.donated)
        self.calculatorWidget.donateButton.clicked.connect(self.onDonateButtonClicked)

    def loadThemeMode(self) -> str:
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        mode = str(settings.value("ui/themeMode", theme.defaultThemeMode))
        return mode if mode in theme.themeModes else theme.defaultThemeMode

    def applyTheme(self, mode: str) -> None:
        self.currentThemeMode = mode
        self.setStyleSheet(theme.windowStyleSheet(mode))
        self.calculatorWidget.applyTheme(mode)

    def onThemeToggled(self, checked: bool) -> None:
        self.onThemeSelected("dark" if checked else "light")

    def onThemeSelected(self, mode: str) -> None:
        self.applyTheme(mode)
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        settings.setValue("ui/themeMode", mode)

    def loadDonated(self) -> bool:
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        return settings.value("support/donated", False, type=bool)

    def markDonated(self) -> None:
        self.donated = True
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        settings.setValue("support/donated", True)
        self.calculatorWidget.donateButton.setVisible(False)
        QMessageBox.information(
            self, "Thank You", "Thank you for supporting the development of this app!"
        )

    def onDonateButtonClicked(self) -> None:
        # Arm the ask-on-return prompt; it fires in changeEvent once the
        # window has lost focus (browser visit) and been activated again.
        self.donatePromptPending = True
        self.donateWindowLeft = False

    def changeEvent(self, event: QEvent) -> None:
        super().changeEvent(event)
        if event.type() != QEvent.Type.ActivationChange or not self.donatePromptPending:
            return
        if not self.isActiveWindow():
            self.donateWindowLeft = True
        elif self.donateWindowLeft:
            self.donatePromptPending = False
            self.donateWindowLeft = False
            # Let the window finish activating before showing a modal.
            QTimer.singleShot(300, self.askDonationConfirmation)

    def askDonationConfirmation(self) -> None:
        answer = QMessageBox.question(
            self,
            "Donation",
            "Did you complete a donation?\nIf so, the Donate button will be hidden.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.markDonated()

    def buildAboutText(self) -> str:
        year = datetime.date.today().year
        return (
            f"<h3>{appConfig.appName}</h3>"
            f"<p>Version {appConfig.appVersion}</p>"
            f"<p>Editor: {appConfig.editorName}<br>"
            f"AI Agent: {appConfig.aiAgentName}</p>"
            f"<p>&copy; {year} {appConfig.copyrightHolder}</p>"
        )

    def buildAboutBox(self) -> QMessageBox:
        aboutBox = QMessageBox(self)
        aboutBox.setWindowTitle(f"About {appConfig.appName}")
        aboutBox.setText(self.buildAboutText())
        # Declared explicitly: adding any custom button (the donated entry)
        # suppresses the automatic Ok.
        aboutBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        iconPixmap = QPixmap(str(appConfig.iconPngPath)).scaled(
            64, 64,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        aboutBox.setIconPixmap(iconPixmap)
        # QMessageBox ignores resize; sizing its text label (only — not every
        # QLabel, or the icon label inflates too) matches the app's width.
        aboutBox.setStyleSheet("QLabel#qt_msgbox_label { min-width: 240px; }")
        return aboutBox

    def onHelpAbout(self) -> None:
        aboutBox = self.buildAboutBox()
        donatedButton = None
        if not self.donated:
            donatedButton = aboutBox.addButton(
                "I Already Donated", QMessageBox.ButtonRole.ActionRole
            )
        aboutBox.exec()
        if donatedButton is not None and aboutBox.clickedButton() is donatedButton:
            self.markDonated()
