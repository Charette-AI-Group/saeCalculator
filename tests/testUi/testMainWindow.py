"""Smoke tests for the main window."""

from __future__ import annotations

from PySide6.QtCore import Qt

from saeCalculator.ui.mainWindow import MainWindow


def testMainWindowOpens(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    mainWindow.show()

    assert mainWindow.isVisible()
    assert mainWindow.windowTitle() == "SAE Fractional Calculator"
    assert mainWindow.statusLabel.text() == "Ready"


def testGreetButtonUpdatesLabel(qtbot) -> None:
    mainWindow = MainWindow()
    qtbot.addWidget(mainWindow)
    mainWindow.show()

    qtbot.mouseClick(mainWindow.greetButton, Qt.MouseButton.LeftButton)

    assert mainWindow.statusLabel.text() == "Hello from SAE Fractional Calculator"
