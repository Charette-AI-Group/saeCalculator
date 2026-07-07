"""Main application window."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from saeCalculator import appConfig


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(appConfig.windowTitle)
        self.resize(appConfig.defaultWindowWidth, appConfig.defaultWindowHeight)

        self.statusLabel = QLabel("Ready")
        self.greetButton = QPushButton("Say Hello")

        self.greetButton.clicked.connect(self.onGreetClicked)

        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self.statusLabel)
        layout.addWidget(self.greetButton)
        layout.addStretch()

        self.setCentralWidget(centralWidget)

    def onGreetClicked(self) -> None:
        self.statusLabel.setText("Hello from SAE Fractional Calculator")
