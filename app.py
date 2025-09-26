import streamlit as st
from utils import sidebar_inputs

st.set_page_config(page_title="Servo Axis Engineering Toolbox", layout="wide")

st.title("⚙️ Servo Axis Engineering Toolbox")
st.write("Multi-page app for sizing linear axes (ball screw), motors, drives & gearboxes.")

st.header("Quick Start")
st.markdown("""
Use the **sidebar** to set your default axis & motor data (lead, masses, Kt, Ke, etc.).  
Then open a page from the left sidebar (e.g., *Axis Sizing* or *Torque–Speed*).
""")

# Render the shared sidebar once on the home page to set defaults in session_state
params = sidebar_inputs()

st.subheader("Current Defaults")
st.json(params)
