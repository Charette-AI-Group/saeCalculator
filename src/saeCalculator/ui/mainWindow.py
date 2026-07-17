"""Main application window."""

from __future__ import annotations

import datetime

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QAction, QActionGroup, QIcon, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
)

from saeCalculator import appConfig
from saeCalculator.ui import theme
from saeCalculator.ui.calculatorWidget import CalculatorWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(appConfig.windowTitle)
        self.setWindowIcon(QIcon(str(appConfig.iconPngPath)))
        self.resize(appConfig.defaultWindowWidth, appConfig.defaultWindowHeight)

        self.buildMenuBar()
        self.statusBar().showMessage("Ready")

        year = datetime.date.today().year
        self.copyrightLabel = QLabel(f"© {year} {appConfig.copyrightHolder}")
        self.copyrightLabel.setObjectName("copyrightLabel")
        self.statusBar().addPermanentWidget(self.copyrightLabel)

        self.calculatorWidget = CalculatorWidget()
        self.setCentralWidget(self.calculatorWidget)
        self.calculatorWidget.setFocus()

        self.applyTheme(self.loadThemeMode())

    def buildMenuBar(self) -> None:
        # Menus are kept as attributes: features can extend them later, and it
        # prevents the Python wrappers from being garbage-collected.
        optionsMenu = self.optionsMenu = self.menuBar().addMenu("&Options")

        self.themeActionGroup = QActionGroup(self)
        self.themeActionGroup.setExclusive(True)

        self.lightModeAction = QAction("&Light Mode", self)
        self.lightModeAction.setCheckable(True)
        self.lightModeAction.triggered.connect(lambda checked=False: self.onThemeSelected("light"))
        self.themeActionGroup.addAction(self.lightModeAction)
        optionsMenu.addAction(self.lightModeAction)

        self.darkModeAction = QAction("&Dark Mode", self)
        self.darkModeAction.setCheckable(True)
        self.darkModeAction.triggered.connect(lambda checked=False: self.onThemeSelected("dark"))
        self.themeActionGroup.addAction(self.darkModeAction)
        optionsMenu.addAction(self.darkModeAction)

        helpMenu = self.helpMenu = self.menuBar().addMenu("&Help")

        self.aboutAction = QAction("&About", self)
        self.aboutAction.triggered.connect(self.onHelpAbout)
        helpMenu.addAction(self.aboutAction)

    def loadThemeMode(self) -> str:
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        mode = str(settings.value("ui/themeMode", theme.defaultThemeMode))
        return mode if mode in theme.themeModes else theme.defaultThemeMode

    def applyTheme(self, mode: str) -> None:
        self.currentThemeMode = mode
        self.setStyleSheet(theme.windowStyleSheet(mode))
        self.calculatorWidget.applyTheme(mode)
        self.lightModeAction.setChecked(mode == "light")
        self.darkModeAction.setChecked(mode == "dark")

    def onThemeSelected(self, mode: str) -> None:
        self.applyTheme(mode)
        settings = QSettings(appConfig.organizationName, appConfig.appName)
        settings.setValue("ui/themeMode", mode)

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
        self.buildAboutBox().exec()
