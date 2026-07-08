"""Fraction calculator engine — entry state machine and integer 1/32-inch arithmetic.

All lengths are held as integer counts of 1/32 inch, so addition and
subtraction are exact. Multiply and divide treat the right operand as a
scalar and round the result to the nearest 1/32.

Key grammar (mirrors the approved keypad mockup): whatever number is
pending becomes yards/feet/inches when a unit key is pressed, or a
numerator when a denominator key ("f2".."f32") is pressed.
"""

from __future__ import annotations

import math
import re

primeSign = "′"  # feet
doublePrimeSign = "″"  # inches
minusSign = "−"
multiplySign = "×"
divideSign = "÷"

unitsPerInch = 32
unitsPerFoot = 12 * unitsPerInch
inchesPerYard = 36

operatorSymbols: dict[str, str] = {
    "op+": "+",
    "op-": minusSign,
    "op*": multiplySign,
    "op/": divideSign,
}

fractionKeys = ("f2", "f4", "f8", "f16", "f32")
unitKeys = ("yd", "ft", "in")


def roundHalfUp(value: float) -> int:
    """Round with halves going up (JavaScript Math.round semantics)."""
    return math.floor(value + 0.5)


def parseNumber(text: str) -> float:
    try:
        return float(text)
    except ValueError:
        return 0.0


def formatNumber(value: float) -> str:
    return str(int(value)) if value == int(value) else str(value)


def formatLength(totalUnits: int | None) -> str:
    """Render a 1/32-inch count as feet-inches with a reduced fraction."""
    if totalUnits is None:
        return "0" + doublePrimeSign
    sign = minusSign if totalUnits < 0 else ""
    feet, remaining = divmod(abs(totalUnits), unitsPerFoot)
    inches, fraction = divmod(remaining, unitsPerInch)
    text = sign
    if feet:
        text += f"{feet}{primeSign} "
    text += str(inches)
    if fraction:
        divisor = math.gcd(fraction, unitsPerInch)
        text += f"-{fraction // divisor}/{unitsPerInch // divisor}"
    return text + doublePrimeSign


class CalculatorEngine:
    """Keypad state machine.

    Accepted keys: digits, ".", unit keys ("yd", "ft", "in"), denominator
    keys ("f2".."f32"), operators ("op+", "op-", "op*", "op/"), "eq",
    "B" (backspace), and "C" (clear).
    """

    def __init__(self) -> None:
        self.clearAll()

    def clearAll(self) -> None:
        self.total: int | None = None
        self.pendingOperator: str | None = None
        self.expression: str = ""
        self.resultShown: bool = False
        self.clearEntry()

    def clearEntry(self) -> None:
        self.buffer: str = ""
        self.yards: float | None = None
        self.feet: float | None = None
        self.inches: float | None = None
        self.numerator: int | None = None
        self.denominator: int | None = None

    @property
    def displayText(self) -> str:
        if self.resultShown:
            return formatLength(self.total)
        if self.hasEntry():
            return self.entryText()
        if self.total is not None:
            return formatLength(self.total)
        return "0" + doublePrimeSign

    @property
    def expressionText(self) -> str:
        return self.expression

    def hasEntry(self) -> bool:
        return (
            self.yards is not None
            or self.feet is not None
            or self.inches is not None
            or self.numerator is not None
            or self.buffer != ""
        )

    def entryValue(self) -> int:
        """Current entry as a 1/32-inch count, rounded onto the grid."""
        inches = (self.inches or 0.0) + (parseNumber(self.buffer) if self.buffer else 0.0)
        fraction = 0.0
        if self.numerator is not None and self.denominator:
            fraction = self.numerator / self.denominator
        totalInches = (
            (self.yards or 0.0) * inchesPerYard + (self.feet or 0.0) * 12 + inches + fraction
        )
        return roundHalfUp(totalInches * unitsPerInch)

    def entryText(self) -> str:
        """Progressive display of the entry being typed, e.g. 1′ 6-1/2″."""
        text = ""
        if self.yards is not None:
            text += f"{formatNumber(self.yards)} yd "
        if self.feet is not None:
            text += f"{formatNumber(self.feet)}{primeSign} "
        if self.inches is not None:
            text += formatNumber(self.inches)
            if self.numerator is not None:
                text += f"-{self.numerator}/{self.denominator}{doublePrimeSign}"
            elif self.buffer:
                text += f"-{self.buffer}"
            else:
                text += doublePrimeSign
        else:
            if self.buffer:
                text += self.buffer
            if self.numerator is not None:
                dash = "-" if self.buffer else ""
                text += f"{dash}{self.numerator}/{self.denominator}{doublePrimeSign}"
        return text

    def press(self, key: str) -> None:
        if key == "C":
            self.clearAll()
        elif key == "B":
            if self.buffer:
                self.buffer = self.buffer[:-1]
        elif key.isdigit() or key == ".":
            self.pressDigit(key)
        elif key in unitKeys:
            self.pressUnit(key)
        elif key in fractionKeys:
            self.pressFraction(key)
        elif key in operatorSymbols:
            self.pressOperator(operatorSymbols[key])
        elif key == "eq":
            self.pressEquals()

    def pressDigit(self, key: str) -> None:
        self.startFreshAfterResult()
        if key == "." and "." in self.buffer:
            return
        self.buffer += key

    def pressUnit(self, key: str) -> None:
        self.startFreshAfterResult()
        value = parseNumber(self.buffer)
        if key == "yd":
            self.yards = value
        elif key == "ft":
            self.feet = value
        else:
            self.inches = value
        self.buffer = ""

    def pressFraction(self, key: str) -> None:
        self.startFreshAfterResult()
        self.numerator = int(parseNumber(self.buffer)) or 1
        self.denominator = int(key[1:])
        self.buffer = ""
        # A bare fraction after ft/yd is inches: 1 ft 1 /2 -> 1' 0-1/2".
        if self.inches is None and (self.feet is not None or self.yards is not None):
            self.inches = 0.0

    def pressOperator(self, symbol: str) -> None:
        if self.resultShown:
            self.resultShown = False
            self.expression = f"{formatLength(self.total)} {symbol} "
            self.pendingOperator = symbol
            return
        if self.hasEntry():
            value = self.entryValue()
            self.expression += f"{self.entryText().strip()} {symbol} "
            if self.total is None or self.pendingOperator is None:
                self.total = value
            else:
                self.total = self.applyOperator(self.total, self.pendingOperator, value)
            self.clearEntry()
        elif self.total is not None:
            operatorClass = f"[+{minusSign}{multiplySign}{divideSign}] $"
            self.expression = re.sub(operatorClass, f"{symbol} ", self.expression)
        self.pendingOperator = symbol

    def pressEquals(self) -> None:
        if not self.hasEntry() and self.total is None:
            return
        value = self.entryValue() if self.hasEntry() else self.total
        if self.pendingOperator is not None and self.hasEntry():
            self.total = self.applyOperator(self.total or 0, self.pendingOperator, value)
            self.expression += f"{self.entryText().strip()} ="
        elif self.pendingOperator is None:
            self.total = value
            entryPart = self.entryText().strip() if self.hasEntry() else formatLength(self.total)
            self.expression = f"{entryPart} ="
        self.pendingOperator = None
        self.clearEntry()
        self.resultShown = True

    def applyOperator(self, left: int, symbol: str, right: int) -> int:
        if symbol == "+":
            return left + right
        if symbol == minusSign:
            return left - right
        if symbol == multiplySign:
            return roundHalfUp(left * right / unitsPerInch)
        if symbol == divideSign:
            return roundHalfUp(left * unitsPerInch / right) if right else left
        return right

    def startFreshAfterResult(self) -> None:
        if self.resultShown:
            self.total = None
            self.expression = ""
            self.resultShown = False
