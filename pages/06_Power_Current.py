import streamlit as st
from utils import sidebar_inputs, core_calcs
import math

st.title("🔋 Power, Current & Voltage")

p = sidebar_inputs()
r = core_calcs(p)

omega = r["n_motor"] * 2*math.pi / 60.0
P_mech = r["T_peak"] * omega

st.write(f"Mechanical power at requirement: **{P_mech:.0f} W**")
st.write(f"RMS current: **{r['I_rms']:.3f} A**, Peak current: **{r['I_peak']:.3f} A** (using Kt)")
st.write(f"Back-EMF @ vmax: **{r['V_emf']:.1f} V**, DC bus: **{p['bus_vdc']:.0f} V**, margin: **{r['V_margin']:.1f} V**")
st.caption("Current ∝ torque; voltage ∝ speed (back-EMF). PWM carrier is fixed; electrical frequency scales with rpm.")
