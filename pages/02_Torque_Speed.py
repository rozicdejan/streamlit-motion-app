import streamlit as st
from streamlit_echarts import st_echarts
from utils import sidebar_inputs, core_calcs

st.title("📈 Torque–Speed Envelope (with Field Weakening)")

p = sidebar_inputs()
r = core_calcs(p)

# Build curves
speeds = list(range(0, int(p["n_max"])+500, 500))
cont = []
peak = []
for n in speeds:
    if n <= p["n_base"]:
        cont.append([n, p["cont_torque_nm"]])
        peak.append([n, p["peak_torque_nm"]])
    else:
        scale = p["n_base"]/n
        cont.append([n, p["cont_torque_nm"]*scale])
        peak.append([n, p["peak_torque_nm"]*scale])

options = {
    "tooltip": {"trigger": "axis"},
    "xAxis": {"name": "Speed (rpm)", "type": "value", "max": p["n_max"]},
    "yAxis": {"name": "Torque (Nm)", "type": "value", "max": max(p['peak_torque_nm'], r['T_peak'])*1.3},
    "series": [
        {"name": "Continuous Torque", "type": "line", "data": cont,
         "lineStyle": {"color": "blue"}, "areaStyle": {"color": "rgba(0,0,255,0.15)"}},
        {"name": "Peak Torque", "type": "line", "data": peak,
         "lineStyle": {"color": "orange"}, "areaStyle": {"color": "rgba(255,165,0,0.15)"}},
        {"name": "Your Requirement", "type": "scatter",
         "data": [[r['n_motor'], r['T_peak']]], "symbolSize": 14, "itemStyle": {"color": "red"}}
    ]
}
st_echarts(options, height="460px")

st.markdown(f"""
- **Your point:** {r['T_peak']:.3f} Nm @ {r['n_motor']:.0f} rpm  
- **Continuous limit:** {p['cont_torque_nm']:.2f} Nm (flat to {p['n_base']:.0f} rpm, then ∝1/n)  
- **Peak limit:** {p['peak_torque_nm']:.2f} Nm (short-term)
""")

if r['T_peak'] <= p['cont_torque_nm']*(p['n_base']/max(r['n_motor'], p['n_base'])):
    st.success("Inside continuous region — strong thermal margin.")
elif r['T_peak'] <= p['peak_torque_nm']*(p['n_base']/max(r['n_motor'], p['n_base'])):
    st.warning("Above continuous but below peak — OK for short duty. Check RMS on Sizing page.")
else:
    st.error("Exceeds peak capability — increase ratio, lower accel, or choose bigger motor.")
