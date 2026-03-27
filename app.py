# ================================
# FINAL FIXED CALCULATOR (NO ERRORS)
# ================================

import streamlit as st
import math

st.set_page_config(page_title="Calculator", layout="centered")

# -------------------------------
# Session State
# -------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Functions
# -------------------------------
def evaluate_expression(expr):
    try:
        expr = expr.replace("^", "**")

        allowed = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log10,
            "sqrt": math.sqrt,
            "factorial": math.factorial
        }

        return eval(expr, {"__builtins__": None}, allowed)
    except:
        return "Error"

def press(val):
    st.session_state.expression += str(val)

def clear():
    st.session_state.expression = ""

def calculate():
    expr = st.session_state.expression
    result = evaluate_expression(expr)

    if result != "Error":
        st.session_state.history.append(f"{expr} = {result}")

    st.session_state.expression = str(result)

# -------------------------------
# UI
# -------------------------------
st.title("🧮 Scientific Calculator")

# Display
st.text_input(
    "Display",
    value=st.session_state.expression,
    key="display_box",
    disabled=True
)

# -------------------------------
# Buttons (ALL UNIQUE KEYS)
# -------------------------------
buttons = [
    ["7", "8", "9", "/", "sin("],
    ["4", "5", "6", "*", "cos("],
    ["1", "2", "3", "-", "tan("],
    ["0", ".", "+", "=", "log("],
    ["(", ")", "sqrt(", "^", "factorial("],
    ["C"]
]

for i, row in enumerate(buttons):
    cols = st.columns(len(row))
    for j, btn in enumerate(row):
        unique_key = f"btn_{i}_{j}_{btn}"   # 🔥 IMPORTANT

        if cols[j].button(btn, key=unique_key):
            if btn == "=":
                calculate()
            elif btn == "C":
                clear()
            else:
                press(btn)

# -------------------------------
# Sidebar History (FIXED)
# -------------------------------
st.sidebar.title("📜 History")

# UNIQUE KEY
if st.sidebar.button("Clear History", key="clear_history_btn"):
    st.session_state.history = []

for i, item in enumerate(reversed(st.session_state.history)):
    hist_key = f"history_{i}_{item}"  # 🔥 IMPORTANT

    if st.sidebar.button(item, key=hist_key):
        st.session_state.expression = item.split("=")[0].strip()
