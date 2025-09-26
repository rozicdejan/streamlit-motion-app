import streamlit as st
from utils import sidebar_inputs, core_calcs

st.title("⚖️ Inertia Match")

p = sidebar_inputs()
r = core_calcs(p)

ratio_inertia = r["J_ref_cm2"] / p["Jm"]
st.write(f"Load/Motor inertia ratio = **{ratio_inertia:.1f}:1**")

if 3 <= ratio_inertia <= 10:
    st.success("Good (inside 3–10:1 guideline).")
elif ratio_inertia < 3:
    st.info("Load is light relative to rotor — still OK; reducer not required.")
else:
    st.warning("Load inertia high — consider higher gear ratio or stiffer mechanics.")
