import streamlit as st
from utils import sidebar_inputs, core_calcs

st.title("📊 Axis Sizing")

p = sidebar_inputs()
r = core_calcs(p)

st.subheader("Kinematics & Dynamics")
st.write(f"Moved mass: **{r['mass']:.2f} kg**")
st.write(f"Screw speed @ vmax: **{r['n_screw']:.0f} rpm**")
st.write(f"Motor speed @ vmax: **{r['n_motor']:.0f} rpm**")

st.subheader("Torques & Currents (motor side)")
st.write(f"Acceleration torque: **{r['T_acc']:.3f} Nm**")
st.write(f"Drag torque: **{r['T_drag']:.3f} Nm**")
if p["vertical"]:
    st.write(f"Gravity torque: **{r['Tg']:.3f} Nm**")
st.write(f"**Peak torque:** {r['T_peak']:.3f} Nm   |   **RMS torque:** {r['T_rms']:.3f} Nm")
st.write(f"**RMS current:** {r['I_rms']:.3f} Arms   |   **Peak current:** {r['I_peak']:.3f} Arms")

st.subheader("Inertia & Backlash")
st.write(f"Reflected inertia @ motor: **{r['J_ref_cm2']:.3f} kg·cm²**")
st.write(f"Linear backlash from gearbox: **≈{r['backlash_um']:.2f} µm**")

st.subheader("Voltage Check")
st.write(f"Back-EMF @ vmax: **{r['V_emf']:.1f} V**   |   DC bus: **{p['bus_vdc']:.0f} V**   |   Margin: **{r['V_margin']:.1f} V**")
