# ================================
# Scientific Calculator Web App
# ================================

import streamlit as st
import math

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Scientific Calculator", layout="centered")

# -------------------------------
# Custom Dark Mode Styling
# -------------------------------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stTextInput>div>div>input {
        font-size: 24px;
        text-align: right;
    }
    button {
        height: 60px;
        width: 100%;
        font-size: 18px !important;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Session State Initialization
# -------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Helper Functions
# -------------------------------

def evaluate_expression(expr):
    try:
        # Replace math functions for eval
        expr = expr.replace("^", "**")
        expr = expr.replace("sqrt", "math.sqrt")
        expr = expr.replace("sin", "math.sin")
        expr = expr.replace("cos", "math.cos")
        expr = expr.replace("tan", "math.tan")
        expr = expr.replace("log", "math.log10")
        expr = expr.replace("factorial", "math.factorial")

        result = eval(expr)
        return result
    except Exception:
        return "Error"


def button_click(value):
    st.session_state.expression += str(value)


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
# Display Screen
# -------------------------------
st.text_input("Display", st.session_state.expression, key="display")

# -------------------------------
# Button Layout
# -------------------------------

buttons = [
    ["7", "8", "9", "/", "sin"],
    ["4", "5", "6", "*", "cos"],
    ["1", "2", "3", "-", "tan"],
    ["0", ".", "+", "=", "log"],
    ["(", ")", "sqrt", "^", "factorial"],
    ["C"]
]

for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        if cols[i].button(btn):
            if btn == "=":
                calculate()
            elif btn == "C":
                clear()
            else:
                button_click(btn)

# -------------------------------
# Sidebar History
# -------------------------------
st.sidebar.title("📜 History")

if st.sidebar.button("Clear History"):
    st.session_state.history = []

for item in reversed(st.session_state.history):
    if st.sidebar.button(item):
        # Reuse expression
        st.session_state.expression = item.split("=")[0].strip()

# -------------------------------
# Keyboard Input Support
# -------------------------------
user_input = st.text_input("Type Expression and Press Enter")

if user_input:
    st.session_state.expression = user_input
    calculate()
