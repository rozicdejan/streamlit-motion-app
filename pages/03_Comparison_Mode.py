import streamlit as st
from streamlit_echarts import st_echarts
from utils import sidebar_inputs, core_calcs

st.title("🔀 Comparison Mode (A vs B)")

# Base params
p = sidebar_inputs()

# Scenario inputs
st.subheader("Scenario A")
colA = st.columns(3)
ratio_A = colA[0].number_input("Ratio A", 0.2, 100.0, p["ratio"], 0.1)
eff_A = colA[1].slider("Efficiency A", 0.80, 1.0, p["eff"])
back_A = colA[2].selectbox("Backlash A (arcmin)", [3,5,8,10], index=[3,5,8,10].index(p["backlash_arcmin"]))

st.subheader("Scenario B")
colB = st.columns(3)
ratio_B = colB[0].number_input("Ratio B", 0.2, 100.0, 2.0, 0.1)
eff_B = colB[1].slider("Efficiency B", 0.80, 1.0, p["eff"], key="effB")
back_B = colB[2].selectbox("Backlash B (arcmin)", [3,5,8,10], index=1, key="backB")

def calc_with_overrides(ratio, eff, back):
    pp = p.copy()
    pp["ratio"], pp["eff"], pp["backlash_arcmin"] = ratio, eff, back
    return core_calcs(pp), pp

A, pA = calc_with_overrides(ratio_A, eff_A, back_A)
B, pB = calc_with_overrides(ratio_B, eff_B, back_B)

st.subheader("Side-by-Side")
st.table({
    "Metric": [
        "Gear Ratio", "Motor Speed @ vmax (rpm)", "Screw Speed @ vmax (rpm)",
        "Peak Torque (Nm)", "RMS Torque (Nm)", "Peak Current (A)", "RMS Current (A)",
        "Back-EMF @ vmax (V)", "Reflected Inertia (kg·cm²)", "Linear Backlash (µm)"
    ],
    "Scenario A": [
        f"{pA['ratio']:.2f}:1", f"{A['n_motor']:.0f}", f"{A['n_screw']:.0f}",
        f"{A['T_peak']:.3f}", f"{A['T_rms']:.3f}", f"{A['I_peak']:.3f}", f"{A['I_rms']:.3f}",
        f"{A['V_emf']:.1f}", f"{A['J_ref_cm2']:.3f}", f"{A['backlash_um']:.2f}"
    ],
    "Scenario B": [
        f"{pB['ratio']:.2f}:1", f"{B['n_motor']:.0f}", f"{B['n_screw']:.0f}",
        f"{B['T_peak']:.3f}", f"{B['T_rms']:.3f}", f"{B['I_peak']:.3f}", f"{B['I_rms']:.3f}",
        f"{B['V_emf']:.1f}", f"{B['J_ref_cm2']:.3f}", f"{B['backlash_um']:.2f}"
    ]
})

st.subheader("Torque–Speed Chart")
options = {
    "tooltip": {"trigger": "axis"},
    "xAxis": {"name": "Speed (rpm)", "type": "value", "max": p["n_max"]},
    "yAxis": {"name": "Torque (Nm)", "type": "value", "max": max(p['peak_torque_nm'], A['T_peak'], B['T_peak'])*1.3},
    "series": [
        {"name": "Scenario A", "type": "scatter", "data": [[A['n_motor'], A['T_peak']]], "symbolSize": 14, "itemStyle": {"color": "red"}},
        {"name": "Scenario B", "type": "scatter", "data": [[B['n_motor'], B['T_peak']]], "symbolSize": 14, "itemStyle": {"color": "green"}},
    ]
}
st_echarts(options, height="420px")
