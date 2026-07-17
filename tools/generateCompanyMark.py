"""Render the company mark SVGs to PNGs in src/saeCalculator/resources.

Run from the repo root:

    python tools/generateCompanyMark.py

The SVG sources (companyMarkLight/Dark.svg) are copies of the wave
variants from the Charette AI Group logo design package; regenerate the
PNGs after changing them. PNGs are used at runtime so the frozen app
does not depend on the Qt SVG plugin.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer

resourcesDir = Path(__file__).resolve().parents[1] / "src" / "saeCalculator" / "resources"
renderSize = 192


def renderToPng(svgPath: Path, pngPath: Path) -> None:
    renderer = QSvgRenderer(str(svgPath))
    image = QImage(renderSize, renderSize, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    image.save(str(pngPath))
    print(f"wrote {pngPath}")


def main() -> None:
    QGuiApplication([])
    for name in ("companyMarkLight", "companyMarkDark"):
        renderToPng(resourcesDir / f"{name}.svg", resourcesDir / f"{name}.png")


if __name__ == "__main__":
    main()
