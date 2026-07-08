"""Application entry point — wiring only."""

from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from saeCalculator import appConfig
from saeCalculator.ui.mainWindow import MainWindow


def main() -> int:
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appConfig.appUserModelId)

    app = QApplication(sys.argv)
    app.setApplicationName(appConfig.appName)
    app.setApplicationVersion(appConfig.appVersion)
    app.setOrganizationName(appConfig.organizationName)
    app.setWindowIcon(QIcon(str(appConfig.iconPngPath)))

    mainWindow = MainWindow()
    mainWindow.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
