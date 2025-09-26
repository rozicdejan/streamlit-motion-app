import streamlit as st
import math
from utils import sidebar_inputs, core_calcs, trapezoid_times

st.title("📐 Duty Cycle & RMS Calculator")

p = sidebar_inputs()

st.subheader("Option A — Enter Segments (torque & time)")
rows = st.number_input("Number of segments", 1, 10, 4)
total_E = 0.0
total_t = 0.0
for i in range(rows):
    c = st.columns(2)
    Ti = c[0].number_input(f"Segment {i+1} torque (Nm)", -10.0, 10.0, 0.2, 0.01, key=f"T{i}")
    ti = c[1].number_input(f"Segment {i+1} time (s)", 0.0, 60.0, 0.25, 0.01, key=f"t{i}")
    total_E += (Ti**2) * ti
    total_t += ti

if total_t > 0:
    T_rms = math.sqrt(total_E/total_t)
    st.write(f"**RMS torque = {T_rms:.3f} Nm** over **{total_t:.3f} s**")

st.markdown("---")
st.subheader("Option B — Trapezoidal Move (auto)")
dist_mm = st.number_input("Move distance (mm)", 0.1, 5000.0, p["stroke_mm"], 0.1)
dist_m = dist_mm/1000.0
ta, tc, td = trapezoid_times(dist_m, p["vmax"], p["accel"])
st.write(f"Accel time **{ta:.3f} s**, cruise **{tc:.3f} s**, decel **{td:.3f} s**")

# Use core_calcs to get torques at accel/cruise/decel (motor side)
from utils import core_calcs
r = core_calcs(p)
T_acc = r["T_drag"] + r["T_acc"] + r["Tg"]
T_cru = r["T_drag"] + r["Tg"]
T_dec = r["T_drag"] + r["Tg"]  # active decel by servo ≈ accel magnitude but opposite sign; RMS uses square

E = (T_acc**2)*ta + (T_cru**2)*tc + (T_dec**2)*td
T_rms_auto = math.sqrt(E/(ta+tc+td))
t_oneway = ta+tc+td
st.write(f"**RMS torque (one move) = {T_rms_auto:.3f} Nm**, move time **{t_oneway:.3f} s**")
