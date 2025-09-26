import streamlit as st
import math

st.title("🧭 Critical Screw Speed")

st.markdown("Estimate screw critical speed (first bending mode). Use root diameter and unsupported length.")

d_mm = st.number_input("Screw root diameter (mm)", 5.0, 80.0, 16.0)
L_mm = st.number_input("Unsupported screw length (mm)", 100.0, 3000.0, 520.0)
fixity = st.selectbox("End fixity", ["Fixed–Free", "Simple–Simple", "Fixed–Simple", "Fixed–Fixed"])

# approximate chart factors (common for ball screws)
K_map = {"Fixed–Free": 3.13, "Simple–Simple": 22.4, "Fixed–Simple": 33.6, "Fixed–Fixed": 65.7}
K = K_map[fixity]
ncrit = (K * d_mm) / ((L_mm/1000.0)**2)  # rpm

st.write(f"Estimated **critical speed ≈ {ncrit:.0f} rpm**")

if ncrit < 1.25 * 4200:
    st.warning("Close to operating speed; keep screw ≤ ~80% of critical speed for safety.")
else:
    st.success("Screw speed target appears comfortably under the critical speed.")
