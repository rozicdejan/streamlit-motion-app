import streamlit as st
import math

st.set_page_config(page_title="Regen & Braking Power", layout="wide")

st.title("⚡ Regeneration / Braking Power Calculator")

st.markdown("""
This tool estimates braking (regen) energy and power for your linear axis,
and compares it with Kollmorgen AKD internal brake resistor capacity.
""")

st.header("Input Parameters")

col1, col2 = st.columns(2)

with col1:
    m_kg = st.number_input("Moved Mass (kg)", 0.0, 100.0, 2.5, step=0.1)
    lead_mm_rev = st.number_input("Screw Lead (mm/rev)", 0.1, 50.0, 16.0, step=0.1)
    eff = st.number_input("Efficiency (%)", 10.0, 100.0, 90.0, step=1.0) / 100.0
    v_mm_s = st.number_input("Max Linear Speed (mm/s)", 1.0, 10000.0, 1120.0, step=10.0)

with col2:
    J_motor = st.number_input("Motor Inertia J (kg·m²)", 0.0, 1e-3, 1.1e-5, step=1e-6, format="%.1e")
    n_motor = st.number_input("Motor Speed at vmax (RPM)", 0.0, 100000.0, 4200.0, step=100.0)
    t_dec = st.number_input("Decel Time (s)", 0.01, 10.0, 0.15, step=0.01)
    n_stops = st.number_input("Stops per Cycle", 1, 100, 8, step=1)
    repeats = st.number_input("Cycle Repeats", 1, 100, 5, step=1)
    t_cycle = st.number_input("Total Cycle Duration (s)", 0.1, 1000.0, 120.0, step=1.0)

# --- Calculations ---
lead_m_rev = lead_mm_rev / 1000.0
v_m_s = v_mm_s / 1000.0
w_motor = n_motor * 2 * math.pi / 60.0

# Kinetic energies
E_lin = 0.5 * m_kg * v_m_s**2
E_rot = 0.5 * J_motor * w_motor**2
E_stop = E_lin + E_rot

P_peak = E_stop / t_dec if t_dec > 0 else 0.0
E_cycle = E_stop * n_stops * repeats
P_avg = E_cycle / t_cycle if t_cycle > 0 else 0.0

# --- Results ---
st.header("Results")
st.write(f"🔹 Linear KE: **{E_lin:.3f} J**")
st.write(f"🔹 Motor Rotor KE: **{E_rot:.3f} J**")
st.write(f"🔹 Energy per stop: **{E_stop:.3f} J**")
st.write(f"🔹 Peak regen power: **{P_peak:.1f} W**")
st.write(f"🔹 Energy per cycle: **{E_cycle:.1f} J**")
st.write(f"🔹 Average regen power: **{P_avg:.2f} W**")

# --- Comparison with AKD ---
st.header("AKD Internal Brake Comparison")
st.markdown("""
- Internal resistor: ~15 Ω  
- Continuous absorption: ~100 W  
- Short peaks: multi-kW capable (datasheet)
""")

if P_peak < 100 and P_avg < 20:
    st.success("✅ Safe: Internal brake resistor is more than sufficient for your profile.")
else:
    st.warning("⚠️ Check: You may need an external regen resistor if mass/speed increases.")

st.markdown("---")
st.caption("Use this page to experiment with different masses, speeds, decel times, and cycle repeats.")
