import streamlit as st
import math

st.title("🏗️ Buckling Load (Euler)")

E = st.number_input("Young's modulus E (GPa)", 100.0, 300.0, 210.0) * 1e3  # MPa→N/mm²
d_mm = st.number_input("Screw root diameter (mm)", 5.0, 80.0, 16.0)
L_mm = st.number_input("Unsupported length (mm)", 100.0, 3000.0, 520.0)
fixity = st.selectbox("End fixity", ["Fixed–Free", "Pinned–Pinned", "Fixed–Pinned", "Fixed–Fixed"])

K_map = {"Fixed–Free": 2.0, "Pinned–Pinned": 1.0, "Fixed–Pinned": 0.7, "Fixed–Fixed": 0.5}
K = K_map[fixity]
I = (math.pi * d_mm**4) / 64.0  # mm^4

Fcr_N = (math.pi**2 * E * I) / ((K * L_mm)**2)  # N
st.write(f"Critical buckling load **≈ {Fcr_N/1000:.1f} kN**")

st.caption("Keep working compressive load well below Fcr (e.g., <40–50%).")
