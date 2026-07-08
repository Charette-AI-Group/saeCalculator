"""Unit tests for the calculator engine state machine."""

from __future__ import annotations

from saeCalculator.services.calculatorEngine import CalculatorEngine, formatLength


def newEngine(keys: list[str] | None = None) -> CalculatorEngine:
    engine = CalculatorEngine()
    for key in keys or []:
        engine.press(key)
    return engine


def testFormatLength() -> None:
    assert formatLength(None) == "0″"
    assert formatLength(0) == "0″"
    assert formatLength(16) == "0-1/2″"
    assert formatLength(384) == "1′ 0″"
    assert formatLength(384 + 8) == "1′ 0-1/4″"
    assert formatLength(-32) == "−1″"


def testFeetInchFractionAddition() -> None:
    engine = newEngine(["1", "ft", "6", "in", "1", "f2", "op+", "2", "ft", "5", "in", "3", "f4"])
    engine.press("eq")

    assert engine.displayText == "4′ 0-1/4″"
    assert engine.expressionText == "1′ 6-1/2″ + 2′ 5-3/4″ ="


def testYardEntryAndSubtraction() -> None:
    keys = ["1", "yd", "2", "ft", "4", "in", "3", "f16", "op-", "1", "0", "in", "5", "f8", "eq"]
    engine = newEngine(keys)

    # 1 yd 2' 4-3/16" = 64.1875"; minus 10.625" = 53.5625" = 4' 5-9/16"
    assert engine.displayText == "4′ 5-9/16″"
    assert engine.expressionText == "1 yd 2′ 4-3/16″ − 10-5/8″ ="


def testDivisionRoundsToNearestThirtySecond() -> None:
    engine = newEngine(["1", "in", "op/", "3", "eq"])

    # 1" / 3 = 10.67/32, rounds to 11/32.
    assert engine.displayText == "0-11/32″"


def testMultiplicationByScalar() -> None:
    engine = newEngine(["2", "in", "1", "f2", "op*", "2", "eq"])

    assert engine.displayText == "5″"


def testFractionOnlyEntry() -> None:
    engine = newEngine(["3", "f8", "eq"])

    assert engine.displayText == "0-3/8″"


def testFractionAfterFeetImpliesZeroInches() -> None:
    engine = newEngine(["1", "ft", "1", "f2"])

    assert engine.displayText == "1′ 0-1/2″"
    engine.press("eq")
    assert engine.displayText == "1′ 0-1/2″"


def testResultFractionIsReduced() -> None:
    engine = newEngine(["1", "f4", "op+", "1", "f4", "eq"])

    assert engine.displayText == "0-1/2″"


def testDecimalInchesConvertToFraction() -> None:
    engine = newEngine(["4", ".", "5", "in", "eq"])

    assert engine.displayText == "4-1/2″"


def testEntryDisplayBuildsProgressively() -> None:
    engine = newEngine()
    steps = [
        ("1", "1"),
        ("ft", "1′ "),
        ("6", "1′ 6"),
        ("in", "1′ 6″"),
        ("1", "1′ 6-1"),
        ("f2", "1′ 6-1/2″"),
    ]
    for key, expected in steps:
        engine.press(key)
        assert engine.displayText == expected


def testDisplayShowsRunningTotalAfterOperator() -> None:
    engine = newEngine(["1", "ft", "op+"])

    assert engine.displayText == "1′ 0″"
    assert engine.expressionText == "1′ + "


def testOperatorPressedTwiceReplacesPrevious() -> None:
    engine = newEngine(["5", "in", "op+", "op-"])

    assert engine.expressionText == "5″ − "
    engine.press("2")
    engine.press("in")
    engine.press("eq")
    assert engine.displayText == "3″"


def testResultFeedsNextCalculation() -> None:
    engine = newEngine(["1", "ft", "eq", "op+", "6", "in", "eq"])

    assert engine.displayText == "1′ 6″"


def testDigitAfterResultStartsFresh() -> None:
    engine = newEngine(["1", "in", "eq", "2"])

    assert engine.displayText == "2"
    assert engine.expressionText == ""


def testNegativeResult() -> None:
    engine = newEngine(["1", "in", "op-", "2", "in", "eq"])

    assert engine.displayText == "−1″"


def testBackspaceEditsBuffer() -> None:
    engine = newEngine(["1", "2", "B"])

    assert engine.displayText == "1"


def testClearResetsEverything() -> None:
    engine = newEngine(["1", "ft", "op+", "2", "in", "C"])

    assert engine.displayText == "0″"
    assert engine.expressionText == ""
    assert engine.total is None
    assert engine.pendingOperator is None


def testSecondDecimalPointIgnored() -> None:
    engine = newEngine(["1", ".", "5", ".", "5"])

    assert engine.displayText == "1.55"
