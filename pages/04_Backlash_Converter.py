import streamlit as st
from utils import sidebar_inputs

st.title("↔ Backlash Converter")

p = sidebar_inputs()
theta_rad = (p["backlash_arcmin"]/60.0) * 3.1415926535/180.0
backlash_um = (theta_rad/(2*3.1415926535)) * p["lead_mm"] * 1000.0

st.write(f"Backlash **{p['backlash_arcmin']} arcmin** on **{p['lead_mm']} mm** lead → **{backlash_um:.2f} µm** linear lost motion.")
st.caption("Tip: 5′ ≈ 3.7 µm; 8′ ≈ 5.9 µm; 10′ ≈ 7.4 µm (for 16 mm lead).")
