"""Smoke tests for the calculator widget."""

from __future__ import annotations

from PySide6.QtCore import Qt

from saeCalculator.ui.calculatorWidget import CalculatorWidget


def testAllKeysPresent(qtbot) -> None:
    widget = CalculatorWidget()
    qtbot.addWidget(widget)

    expectedKeys = {
        "C", "yd", "ft", "in",
        "f2", "f4", "f8", "f16", "f32",
        "7", "8", "9", "op/",
        "4", "5", "6", "op*",
        "1", "2", "3", "op-",
        "0", ".", "B", "op+",
        "eq",
    }
    assert set(widget.keyButtons) == expectedKeys


def testExampleCalculationByClicks(qtbot) -> None:
    widget = CalculatorWidget()
    qtbot.addWidget(widget)
    widget.show()

    keys = ["1", "ft", "6", "in", "1", "f2", "op+", "2", "ft", "5", "in", "3", "f4", "eq"]
    for key in keys:
        qtbot.mouseClick(widget.keyButtons[key], Qt.MouseButton.LeftButton)

    assert widget.currentLabel.text() == "4′ 0-1/4″"
    assert widget.expressionLabel.text() == "1′ 6-1/2″ + 2′ 5-3/4″ ="


def testKeyboardEntry(qtbot) -> None:
    widget = CalculatorWidget()
    qtbot.addWidget(widget)
    widget.show()

    # 3" + 2" = 5" typed on the keyboard (i commits inches, = evaluates).
    qtbot.keyClicks(widget, "3i+2i=")

    assert widget.currentLabel.text() == "5″"


def testDonateButtonOpensPaypal(qtbot, monkeypatch) -> None:
    from saeCalculator import appConfig
    from saeCalculator.ui import calculatorWidget as calculatorWidgetModule

    widget = CalculatorWidget()
    qtbot.addWidget(widget)
    widget.show()

    openedUrls = []
    monkeypatch.setattr(
        calculatorWidgetModule.QDesktopServices,
        "openUrl",
        staticmethod(lambda url: openedUrls.append(url.toString())),
    )

    qtbot.mouseClick(widget.donateButton, Qt.MouseButton.LeftButton)
    assert openedUrls == [appConfig.donateUrl]


def testEscapeClears(qtbot) -> None:
    widget = CalculatorWidget()
    qtbot.addWidget(widget)
    widget.show()

    qtbot.keyClicks(widget, "12f")
    assert widget.currentLabel.text() == "12′ "

    qtbot.keyClick(widget, Qt.Key.Key_Escape)
    assert widget.currentLabel.text() == "0″"
