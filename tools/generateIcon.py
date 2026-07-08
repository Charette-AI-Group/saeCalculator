"""Generate the app icon (PNG + multi-size ICO) into src/saeCalculator/resources.

Run from the repo root:

    python tools/generateIcon.py

Requires PySide6 (runtime dependency) and Pillow (in the "build" extra).
The design is a tape-measure-yellow tile with ruler ticks and a stacked
1/2 fraction — the app's entry grammar in one picture.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QFont, QGuiApplication, QImage, QPainter, QPainterPath

repoRoot = Path(__file__).resolve().parents[1]
resourcesDir = repoRoot / "src" / "saeCalculator" / "resources"

backgroundColor = QColor("#f0b232")
inkColor = QColor("#1f1e1b")

icoSizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def renderIcon() -> QImage:
    image = QImage(256, 256, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    tile = QPainterPath()
    tile.addRoundedRect(8, 8, 240, 240, 52, 52)
    painter.fillPath(tile, backgroundColor)
    painter.setClipPath(tile)

    # Ruler ticks along the top edge, alternating major/minor.
    painter.setBrush(inkColor)
    painter.setPen(Qt.PenStyle.NoPen)
    for index in range(9):
        x = 24 + index * 26
        tickHeight = 34 if index % 2 == 0 else 20
        painter.drawRect(x, 8, 8, tickHeight)

    # Stacked 1/2 fraction.
    font = QFont("Arial")
    font.setBold(True)
    font.setPixelSize(86)
    painter.setFont(font)
    painter.setPen(inkColor)
    painter.drawText(QRect(0, 44, 256, 84), Qt.AlignmentFlag.AlignCenter, "1")
    painter.drawText(QRect(0, 150, 256, 84), Qt.AlignmentFlag.AlignCenter, "2")

    barPath = QPainterPath()
    barPath.addRoundedRect(76, 130, 104, 14, 7, 7)
    painter.fillPath(barPath, inkColor)

    painter.end()
    return image


def main() -> None:
    QGuiApplication([])
    resourcesDir.mkdir(parents=True, exist_ok=True)

    pngPath = resourcesDir / "icon.png"
    icoPath = resourcesDir / "icon.ico"

    renderIcon().save(str(pngPath))
    Image.open(pngPath).save(icoPath, sizes=icoSizes)
    print(f"wrote {pngPath}")
    print(f"wrote {icoPath}")


if __name__ == "__main__":
    main()
