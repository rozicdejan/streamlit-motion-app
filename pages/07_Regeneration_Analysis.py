# pages/07_Regeneration_Analysis.py

import streamlit as st
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Regeneration Power Analysis", layout="wide")

st.title("⚡ Regeneration Power Analysis")
st.write("""
This tool calculates and visualizes regenerative braking power for your linear axis motion profile.
It compares **1:1 direct drive** vs. **2:1 reducer**.
""")

# ------------------------
# Constants from your project
# ------------------------
brake_time = 0.15     # [s] braking duration
cycle_time = 18.5     # [s] full cycle with dwell
n_stops = 20          # 5× super-cycle with 4 stops each

# energies per stop [J]
E_stop_1to1 = 3.26
E_stop_2to1 = 5.85

# total energy per cycle
E_cycle_1to1 = E_stop_1to1 * n_stops
E_cycle_2to1 = E_stop_2to1 * n_stops

# average power
P_avg_1to1 = E_cycle_1to1 / cycle_time
P_avg_2to1 = E_cycle_2to1 / cycle_time

# peak power
P_peak_1to1 = E_stop_1to1 / brake_time
P_peak_2to1 = E_stop_2to1 / brake_time

# ------------------------
# Build simplified regen profile (time series)
# ------------------------
time_points = [0]
power_1to1 = [0]
power_2to1 = [0]

t = 0.0
for i in range(n_stops):
    # braking event
    t += 1.0   # move + accel time placeholder
    time_points.append(t)
    power_1to1.append(P_peak_1to1)
    power_2to1.append(P_peak_2to1)

    t += brake_time
    time_points.append(t)
    power_1to1.append(0)
    power_2to1.append(0)

# extend to full cycle time
time_points.append(cycle_time)
power_1to1.append(0)
power_2to1.append(0)

# ------------------------
# ECharts options
# ------------------------
options = {
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["1:1 Direct Drive", "2:1 Reducer"]},
    "xAxis": {"type": "value", "name": "Time [s]"},
    "yAxis": {"type": "value", "name": "Power [W]"},
    "series": [
        {
            "name": "1:1 Direct Drive",
            "type": "line",
            "step": "end",
            "data": [[time_points[i], power_1to1[i]] for i in range(len(time_points))],
        },
        {
            "name": "2:1 Reducer",
            "type": "line",
            "step": "end",
            "data": [[time_points[i], power_2to1[i]] for i in range(len(time_points))],
        },
    ],
}

st.subheader("📊 Regeneration Power vs. Time")
st_echarts(options=options, height="400px")

# ------------------------
# Summary
# ------------------------
st.subheader("🔎 Summary")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 1:1 Direct Drive")
    st.write(f"- Energy per stop: **{E_stop_1to1:.2f} J**")
    st.write(f"- Cycle energy: **{E_cycle_1to1:.1f} J**")
    st.write(f"- Avg power: **{P_avg_1to1:.2f} W**")
    st.write(f"- Peak power: **{P_peak_1to1:.1f} W**")

with col2:
    st.markdown("### 2:1 Reducer")
    st.write(f"- Energy per stop: **{E_stop_2to1:.2f} J**")
    st.write(f"- Cycle energy: **{E_cycle_2to1:.1f} J**")
    st.write(f"- Avg power: **{P_avg_2to1:.2f} W**")
    st.write(f"- Peak power: **{P_peak_2to1:.1f} W**")

st.success("""
**Conclusion:**  
Both cases are far below the AKD internal resistor capacity (100 W continuous, >1 kW peak).  
No external resistor required.
""")
