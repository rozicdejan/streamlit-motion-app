import streamlit as st
from utils import sidebar_inputs, core_calcs

st.title("🌡️ Thermal Check (quick estimate)")

p = sidebar_inputs()
r = core_calcs(p)

ratio = r["T_rms"] / p["cont_torque_nm"]
st.write(f"RMS/Continuous torque ratio **= {ratio:.2f}**")

if ratio <= 1.0:
    st.success("RMS torque ≤ continuous rating — thermally OK for continuous duty.")
else:
    st.error("RMS torque above continuous rating — reduce load/accel, add gearbox, or choose larger motor.")

st.caption("This is a simplified check. For precise thermal models use the motor datasheet and drive thermal tools.")
