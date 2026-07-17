"""Animated on/off slide switch (used for the light/dark theme toggle)."""

from __future__ import annotations

from PySide6.QtCore import Property, QPropertyAnimation, QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QAbstractButton, QWidget


class ToggleSwitch(QAbstractButton):
    """Checkable pill-shaped switch: knob left = off, knob right = on."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # Never take focus so typing keeps reaching the calculator.
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.trackOffColor = QColor("#b9b7af")
        self.trackOnColor = QColor("#185fa5")
        self.knobColor = QColor("#ffffff")
        self._knobPosition = 0.0
        self.knobAnimation = QPropertyAnimation(self, b"knobPosition", self)
        self.knobAnimation.setDuration(120)
        self.toggled.connect(self.animateKnob)

    def sizeHint(self) -> QSize:
        return QSize(46, 24)

    def getKnobPosition(self) -> float:
        return self._knobPosition

    def setKnobPosition(self, value: float) -> None:
        self._knobPosition = value
        self.update()

    knobPosition = Property(float, getKnobPosition, setKnobPosition)

    def setTrackColors(self, offColor: QColor, onColor: QColor) -> None:
        self.trackOffColor = offColor
        self.trackOnColor = onColor
        self.update()

    def animateKnob(self, checked: bool) -> None:
        target = 1.0 if checked else 0.0
        self.knobAnimation.stop()
        if not self.isVisible():
            self.setKnobPosition(target)
            return
        self.knobAnimation.setEndValue(target)
        self.knobAnimation.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        fraction = self._knobPosition
        trackColor = QColor(
            round(self.trackOffColor.red() * (1 - fraction) + self.trackOnColor.red() * fraction),
            round(
                self.trackOffColor.green() * (1 - fraction) + self.trackOnColor.green() * fraction
            ),
            round(self.trackOffColor.blue() * (1 - fraction) + self.trackOnColor.blue() * fraction),
        )
        radius = self.height() / 2
        painter.setBrush(trackColor)
        painter.drawRoundedRect(self.rect(), radius, radius)

        margin = 3
        knobDiameter = self.height() - 2 * margin
        knobX = margin + (self.width() - knobDiameter - 2 * margin) * fraction
        painter.setBrush(self.knobColor)
        painter.drawEllipse(round(knobX), margin, knobDiameter, knobDiameter)
