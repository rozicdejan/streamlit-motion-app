# pages/08_Regeneration_Resistor.py

import streamlit as st
import math
from utils import sidebar_inputs, core_calcs, trapezoid_times  # <-- reuse your functions

st.set_page_config(page_title="Regeneration Resistor Sizing", layout="wide")

st.title("⚡ Regeneration Resistor Sizing")
st.write("""
This tool estimates whether you need an **external regeneration resistor** based on your 
motion profile and axis parameters. It compares **average regen power** and **peak power**
to your drive’s internal resistor capacity.
""")

# --------------------------------------
# Shared inputs
# --------------------------------------
params = sidebar_inputs()
calcs = core_calcs(params)

st.subheader("📥 Motion Inputs")
distance_mm = st.number_input("Stroke distance per move [mm]", 1.0, 2000.0, 320.0, 1.0)
n_moves = st.number_input("Number of moves per cycle", 1, 100, 10)
cycle_dwell = st.number_input("Cycle dwell time [s]", 0.0, 60.0, 15.0, 0.1)

# convert
distance_m = distance_mm / 1000.0

# --------------------------------------
# Motion profile
# --------------------------------------
ta, tc, td = trapezoid_times(distance_m, params["vmax"], params["accel"])
t_move = ta + tc + td
t_cycle = n_moves*t_move + cycle_dwell

# Kinetic energy of payload + carriage
M = params["payload_kg"] + params["carriage_kg"]
vmax = params["vmax"]
E_kin = 0.5*M*vmax**2   # Joules

# regen per stop (assume nearly all KE returned)
E_stop = E_kin * params["screw_eta"]

# total cycle energy
E_cycle = E_stop * n_moves
P_avg = E_cycle / t_cycle
P_peak = E_stop / td if td > 0 else E_stop / ta

# --------------------------------------
# Resistor thresholds (AKD typical)
# --------------------------------------
P_cont_limit = 100.0   # W continuous
P_peak_limit = 1000.0  # W peak (short bursts)

# --------------------------------------
# Display results
# --------------------------------------
st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)
col1.metric("Energy per stop", f"{E_stop:.2f} J")
col2.metric("Total per cycle", f"{E_cycle:.1f} J")
col3.metric("Cycle time", f"{t_cycle:.2f} s")

col4, col5 = st.columns(2)
col4.metric("Average Regen Power", f"{P_avg:.2f} W")
col5.metric("Peak Regen Power", f"{P_peak:.1f} W")

st.subheader("✅ Safety Check")
if P_avg < P_cont_limit and P_peak < P_peak_limit:
    st.success("Internal resistor is sufficient. No external resistor required.")
else:
    st.error("⚠️ External resistor may be needed. Check drive datasheet.")

# --------------------------------------
# Details
# --------------------------------------
with st.expander("Show Detailed Calculations"):
    st.write(f"- Accel time: {ta:.3f} s")
    st.write(f"- Cruise time: {tc:.3f} s")
    st.write(f"- Decel time: {td:.3f} s")
    st.write(f"- Move time: {t_move:.3f} s")
    st.write(f"- Kinetic energy (axis+load): {E_kin:.2f} J")
    st.write(f"- Screw efficiency: {params['screw_eta']:.2f}")
    st.write(f"- Energy recovered per stop: {E_stop:.2f} J")
    st.write(f"- Total energy per cycle: {E_cycle:.1f} J")
    st.write(f"- Average regen power: {P_avg:.2f} W")
    st.write(f"- Peak regen power: {P_peak:.1f} W")
