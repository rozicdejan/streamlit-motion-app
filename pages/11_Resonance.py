import streamlit as st
import math
from utils import sidebar_inputs

st.title("🎵 Resonance (First Mode)")

p = sidebar_inputs()
M = p["payload_kg"] + p["carriage_kg"]

stiff_kNmm = st.number_input("Effective axis stiffness (kN/mm)", 0.1, 50.0, 1.5, 0.1)
k_Nm = stiff_kNmm * 1e6  # kN/mm → N/m

fn = (1/(2*math.pi)) * math.sqrt(k_Nm / M)

st.write(f"Estimated **natural frequency ≈ {fn:.1f} Hz**")
st.info("Rule: keep closed-loop bandwidth ≤ ~fn/5 to avoid ringing.")

st.markdown("""
**What affects fn?**  
- ↑ Stiffness (thicker base, bracing, shorter overhangs) → ↑ fn  
- ↓ Moved mass (lighter tooling) → ↑ fn  
- Gearbox helps servo tuning (torque & inertia) but **does not change the structural fn**.
""")
