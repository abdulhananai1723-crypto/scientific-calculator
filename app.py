# ================================
# Advanced Scientific Calculator
# ================================

import streamlit as st
import math

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Scientific Calculator", layout="centered")

# -------------------------------
# Styling (Dark Mode)
# -------------------------------
st.markdown("""
<style>
.stTextInput input {
    font-size: 28px !important;
    text-align: right;
}
button {
    height: 60px;
    font-size: 18px !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Safe Evaluation
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
            "factorial": math.factorial,
            "pi": math.pi,
            "e": math.e
        }

        result = eval(expr, {"__builtins__": None}, allowed)
        return result
    except:
        return "Error"

# -------------------------------
# Button Functions
# -------------------------------
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
# Title
# -------------------------------
st.title("🧮 Scientific Calculator")

# -------------------------------
# Display (FIXED)
# -------------------------------
st.session_state.expression = st.text_input(
    "Display",
    value=st.session_state.expression,
    key="display"
)

# -------------------------------
# Buttons Layout
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
        if cols[j].button(btn, key=f"btn_{i}_{j}"):
            if btn == "=":
                calculate()
            elif btn == "C":
                clear()
            else:
                press(btn)

# -------------------------------
# Sidebar History
# -------------------------------
st.sidebar.title("📜 History")

if st.sidebar.button("Clear History"):
    st.session_state.history = []

for i, item in enumerate(reversed(st.session_state.history)):
    if st.sidebar.button(item, key=f"hist_{i}"):
        st.session_state.expression = item.split("=")[0].strip()

# -------------------------------
# Keyboard Input
# -------------------------------
user_input = st.text_input("Type Expression & Press Enter")

if user_input:
    st.session_state.expression = user_input
    calculate()
