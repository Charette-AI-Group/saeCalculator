"use strict";

/* JS port of src/saeCalculator/services/calculatorEngine.py — keep in sync.
   All lengths are integer counts of 1/32 inch; results always format as
   feet-inches with reduced fractions. */

const primeSign = "′";
const doublePrimeSign = "″";
const minusSign = "−";
const multiplySign = "×";
const divideSign = "÷";

const unitsPerInch = 32;
const unitsPerFoot = 12 * unitsPerInch;
const inchesPerYard = 36;

const operatorSymbols = { "op+": "+", "op-": minusSign, "op*": multiplySign, "op/": divideSign };
const fractionKeys = ["f2", "f4", "f8", "f16", "f32"];
const unitKeys = ["yd", "ft", "in"];

const donateUrl = "https://www.paypal.com/donate/?hosted_button_id=FEM4WLD7LHY36";

function roundHalfUp(value) { return Math.floor(value + 0.5); }

function parseNumber(text) {
  const value = parseFloat(text);
  return Number.isNaN(value) ? 0 : value;
}

function greatestCommonDivisor(a, b) { return b ? greatestCommonDivisor(b, a % b) : a; }

function formatLength(totalUnits) {
  if (totalUnits === null) return "0" + doublePrimeSign;
  const sign = totalUnits < 0 ? minusSign : "";
  let remaining = Math.abs(Math.round(totalUnits));
  const feet = Math.floor(remaining / unitsPerFoot);
  remaining %= unitsPerFoot;
  const inches = Math.floor(remaining / unitsPerInch);
  const fraction = remaining % unitsPerInch;
  let text = sign;
  if (feet) text += `${feet}${primeSign} `;
  text += inches;
  if (fraction) {
    const divisor = greatestCommonDivisor(fraction, unitsPerInch);
    text += `-${fraction / divisor}/${unitsPerInch / divisor}`;
  }
  return text + doublePrimeSign;
}

class CalculatorEngine {
  constructor() { this.clearAll(); }

  clearAll() {
    this.total = null;
    this.pendingOperator = null;
    this.expression = "";
    this.resultShown = false;
    this.clearEntry();
  }

  clearEntry() {
    this.buffer = "";
    this.yards = null;
    this.feet = null;
    this.inches = null;
    this.numerator = null;
    this.denominator = null;
  }

  get displayText() {
    if (this.resultShown) return formatLength(this.total);
    if (this.hasEntry()) return this.entryText();
    if (this.total !== null) return formatLength(this.total);
    return "0" + doublePrimeSign;
  }

  hasEntry() {
    return this.yards !== null || this.feet !== null || this.inches !== null
      || this.numerator !== null || this.buffer !== "";
  }

  entryValue() {
    const inches = (this.inches || 0) + (this.buffer ? parseNumber(this.buffer) : 0);
    let fraction = 0;
    if (this.numerator !== null && this.denominator) fraction = this.numerator / this.denominator;
    const totalInches = (this.yards || 0) * inchesPerYard + (this.feet || 0) * 12
      + inches + fraction;
    return roundHalfUp(totalInches * unitsPerInch);
  }

  entryText() {
    let text = "";
    if (this.yards !== null) text += `${this.yards} yd `;
    if (this.feet !== null) text += `${this.feet}${primeSign} `;
    if (this.inches !== null) {
      text += `${this.inches}`;
      if (this.numerator !== null) text += `-${this.numerator}/${this.denominator}${doublePrimeSign}`;
      else if (this.buffer) text += `-${this.buffer}`;
      else text += doublePrimeSign;
    } else {
      if (this.buffer) text += this.buffer;
      if (this.numerator !== null) {
        const dash = this.buffer ? "-" : "";
        text += `${dash}${this.numerator}/${this.denominator}${doublePrimeSign}`;
      }
    }
    return text;
  }

  press(key) {
    if (key === "C") { this.clearAll(); return; }
    if (key === "B") {
      if (this.buffer) this.buffer = this.buffer.slice(0, -1);
      return;
    }
    if (/^[0-9.]$/.test(key)) { this.pressDigit(key); return; }
    if (unitKeys.includes(key)) { this.pressUnit(key); return; }
    if (fractionKeys.includes(key)) { this.pressFraction(key); return; }
    if (operatorSymbols[key]) { this.pressOperator(operatorSymbols[key]); return; }
    if (key === "eq") this.pressEquals();
  }

  pressDigit(key) {
    this.startFreshAfterResult();
    if (key === "." && this.buffer.includes(".")) return;
    this.buffer += key;
  }

  pressUnit(key) {
    this.startFreshAfterResult();
    const value = parseNumber(this.buffer);
    if (key === "yd") this.yards = value;
    else if (key === "ft") this.feet = value;
    else this.inches = value;
    this.buffer = "";
  }

  pressFraction(key) {
    this.startFreshAfterResult();
    this.numerator = Math.trunc(parseNumber(this.buffer)) || 1;
    this.denominator = parseInt(key.slice(1), 10);
    this.buffer = "";
    if (this.inches === null && (this.feet !== null || this.yards !== null)) this.inches = 0;
  }

  pressOperator(symbol) {
    if (this.resultShown) {
      this.resultShown = false;
      this.expression = `${formatLength(this.total)} ${symbol} `;
      this.pendingOperator = symbol;
      return;
    }
    if (this.hasEntry()) {
      const value = this.entryValue();
      this.expression += `${this.entryText().trim()} ${symbol} `;
      this.total = (this.total === null || this.pendingOperator === null)
        ? value
        : this.applyOperator(this.total, this.pendingOperator, value);
      this.clearEntry();
    } else if (this.total !== null) {
      this.expression = this.expression.replace(/[+−×÷] $/, `${symbol} `);
    }
    this.pendingOperator = symbol;
  }

  pressEquals() {
    if (!this.hasEntry() && this.total === null) return;
    const value = this.hasEntry() ? this.entryValue() : this.total;
    if (this.pendingOperator !== null && this.hasEntry()) {
      this.total = this.applyOperator(this.total || 0, this.pendingOperator, value);
      this.expression += `${this.entryText().trim()} =`;
    } else if (this.pendingOperator === null) {
      this.total = value;
      const entryPart = this.hasEntry() ? this.entryText().trim() : formatLength(this.total);
      this.expression = `${entryPart} =`;
    }
    this.pendingOperator = null;
    this.clearEntry();
    this.resultShown = true;
  }

  applyOperator(left, symbol, right) {
    if (symbol === "+") return left + right;
    if (symbol === minusSign) return left - right;
    if (symbol === multiplySign) return roundHalfUp(left * right / unitsPerInch);
    if (symbol === divideSign) return right ? roundHalfUp(left * unitsPerInch / right) : left;
    return right;
  }

  startFreshAfterResult() {
    if (this.resultShown) {
      this.total = null;
      this.expression = "";
      this.resultShown = false;
    }
  }
}

/* ---- UI wiring ---- */

const engine = new CalculatorEngine();
const expressionEl = document.getElementById("expression");
const currentEl = document.getElementById("current");
const themeToggle = document.getElementById("themeToggle");
const companyMark = document.getElementById("companyMark");
const donateButton = document.getElementById("donateButton");
const modalOverlay = document.getElementById("modalOverlay");
const modalBody = document.getElementById("modalBody");
const modalButtons = document.getElementById("modalButtons");

function refreshDisplay() {
  expressionEl.textContent = engine.expression;
  currentEl.textContent = engine.displayText;
}

function pressKey(key) {
  engine.press(key);
  refreshDisplay();
}

document.querySelectorAll("[data-k]").forEach((button) => {
  button.addEventListener("mousedown", (event) => event.preventDefault());
  button.addEventListener("click", () => pressKey(button.dataset.k));
});

/* Theme */

function applyTheme(mode) {
  document.documentElement.dataset.theme = mode;
  themeToggle.setAttribute("aria-checked", mode === "dark" ? "true" : "false");
  companyMark.src = mode === "dark" ? "companyMarkDark.svg" : "companyMarkLight.svg";
  localStorage.setItem("themeMode", mode);
}

themeToggle.addEventListener("click", () => {
  applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
});

const savedTheme = localStorage.getItem("themeMode");
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
applyTheme(savedTheme === "dark" || savedTheme === "light" ? savedTheme : (prefersDark ? "dark" : "light"));

/* Modal */

function showModal(bodyHtml, buttons) {
  modalBody.innerHTML = bodyHtml;
  modalButtons.innerHTML = "";
  buttons.forEach((spec) => {
    const button = document.createElement("button");
    button.textContent = spec.label;
    button.className = "modalButton" + (spec.primary ? " primary" : "");
    button.addEventListener("click", () => {
      modalOverlay.classList.add("hidden");
      if (spec.onClick) spec.onClick();
    });
    modalButtons.appendChild(button);
  });
  modalOverlay.classList.remove("hidden");
}

/* Donate (honor system, mirrors the desktop app) */

let donated = localStorage.getItem("donated") === "true";
let donatePromptPending = false;
let donateWindowLeft = false;

function updateDonateVisibility() {
  donateButton.style.display = donated ? "none" : "";
}

function markDonated() {
  donated = true;
  localStorage.setItem("donated", "true");
  updateDonateVisibility();
  showModal("<p>Thank you for supporting the development of this app!</p>",
    [{ label: "OK", primary: true }]);
}

donateButton.addEventListener("click", () => {
  window.open(donateUrl, "_blank", "noopener");
  donatePromptPending = true;
  donateWindowLeft = false;
});

window.addEventListener("blur", () => {
  if (donatePromptPending) donateWindowLeft = true;
});

window.addEventListener("focus", () => {
  if (donatePromptPending && donateWindowLeft) {
    donatePromptPending = false;
    donateWindowLeft = false;
    setTimeout(() => {
      showModal("<p>Did you complete a donation?<br>If so, the Donate button will be hidden.</p>", [
        { label: "Yes", onClick: markDonated },
        { label: "No", primary: true },
      ]);
    }, 300);
  }
});

updateDonateVisibility();

/* About */

document.getElementById("companyButton").addEventListener("click", () => {
  const year = new Date().getFullYear();
  const aboutButtons = [{ label: "OK", primary: true }];
  if (!donated) aboutButtons.unshift({ label: "I Already Donated", onClick: markDonated });
  showModal(`
    <img src="icon.png" alt="" width="56" height="56">
    <h3>SAE Fractional Calculator</h3>
    <p class="muted">Web Edition</p>
    <p>Editor: Francois Charette<br>AI Agent: Claude - Fable 5</p>
    <p>&copy; ${year} Charette AI Group, LLC</p>`, aboutButtons);
});

/* Keyboard */

const keyboardShortcuts = {
  "+": "op+", "-": "op-", "*": "op*", "/": "op/", "=": "eq",
  "y": "yd", "f": "ft", "i": "in", "'": "ft", '"': "in",
};

document.addEventListener("keydown", (event) => {
  if (event.ctrlKey || event.metaKey || event.altKey) return;
  if (!modalOverlay.classList.contains("hidden")) return;
  let key = null;
  if (/^[0-9.]$/.test(event.key)) key = event.key;
  else if (event.key === "Enter") key = "eq";
  else if (event.key === "Backspace") key = "B";
  else if (event.key === "Escape" || event.key === "Delete") key = "C";
  else key = keyboardShortcuts[event.key] || keyboardShortcuts[event.key.toLowerCase()] || null;
  if (key) {
    event.preventDefault();
    pressKey(key);
  }
});

document.getElementById("footerYear").textContent = new Date().getFullYear();
refreshDisplay();
