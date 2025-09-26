import streamlit as st
import math

def sidebar_inputs():
    """Render sidebar inputs and return a params dict. Keeps values in session_state."""
    st.sidebar.header("Shared Axis & Motor Parameters")

    lead_mm = st.sidebar.number_input("Screw lead (mm/rev)", 1.0, 50.0, 16.0, 0.1, key="lead_mm")
    stroke_mm = st.sidebar.number_input("Stroke (mm)", 50.0, 3000.0, 520.0, 1.0, key="stroke_mm")
    payload_kg = st.sidebar.number_input("Payload mass (kg)", 0.0, 200.0, 2.0, 0.1, key="payload_kg")
    carriage_kg = st.sidebar.number_input("Carriage mass (kg)", 0.0, 200.0, 1.58, 0.01, key="carriage_kg")

    accel = st.sidebar.number_input("Acceleration (m/s²)", 0.1, 200.0, 4.825, 0.1, key="accel")
    vmax = st.sidebar.number_input("Max linear speed (m/s)", 0.01, 20.0, 1.12, 0.01, key="vmax")

    Kt = st.sidebar.number_input("Motor torque constant Kt (Nm/Arms)", 0.05, 5.0, 0.304, 0.001, key="Kt")
    Ke = st.sidebar.number_input("Motor voltage constant Ke (V/krpm)", 1.0, 200.0, 19.5, 0.1, key="Ke")
    Jm = st.sidebar.number_input("Motor rotor inertia (kg·cm²)", 0.001, 50.0, 0.11, 0.001, key="Jm")

    ratio = st.sidebar.number_input("Gear ratio (motor:screw)", 0.2, 100.0, 1.0, 0.1, key="ratio")
    eff = st.sidebar.slider("Gearbox efficiency", 0.80, 1.0, 0.97, key="eff")
    backlash_arcmin = st.sidebar.selectbox("Gearbox backlash (arcmin)", [3, 5, 8, 10], key="backlash_arcmin")

    vertical = st.sidebar.checkbox("Vertical axis (gravity)", False, key="vertical")
    screw_eta = st.sidebar.slider("Ball screw efficiency", 0.50, 0.99, 0.90, 0.01, key="screw_eta")
    drag_nom_nm = st.sidebar.number_input("Drag / friction torque at screw (Nm)", 0.0, 5.0, 0.20, 0.01, key="drag_nm")

    bus_vdc = st.sidebar.number_input("Drive DC bus (Vdc)", 50.0, 800.0, 320.0, 1.0, key="bus_vdc")
    cont_torque_nm = st.sidebar.number_input("Motor continuous torque (Nm)", 0.01, 50.0, 0.48, 0.01, key="cont_torque")
    peak_torque_nm = st.sidebar.number_input("Motor peak torque (Nm)", 0.01, 100.0, 1.50, 0.01, key="peak_torque")
    n_base = st.sidebar.number_input("Base speed for field weakening (rpm)", 100.0, 20000.0, 2500.0, 10.0, key="n_base")
    n_max = st.sidebar.number_input("Max mechanical speed (rpm)", 100.0, 60000.0, 8000.0, 10.0, key="n_max")

    return dict(
        lead_mm=lead_mm, stroke_mm=stroke_mm, payload_kg=payload_kg, carriage_kg=carriage_kg,
        accel=accel, vmax=vmax, Kt=Kt, Ke=Ke, Jm=Jm, ratio=ratio, eff=eff,
        backlash_arcmin=backlash_arcmin, vertical=vertical, screw_eta=screw_eta,
        drag_nom_nm=drag_nom_nm, bus_vdc=bus_vdc, cont_torque_nm=cont_torque_nm,
        peak_torque_nm=peak_torque_nm, n_base=n_base, n_max=n_max
    )

def core_calcs(p):
    """Return derived metrics used across pages."""
    M = p["payload_kg"] + p["carriage_kg"]
    lead_m = p["lead_mm"] / 1000.0

    # Load inertia at screw (kg·m²) with screw efficiency
    J_load = (M * (lead_m/(2*math.pi))**2) / p["screw_eta"]
    # Reflected to motor (kg·cm²)
    J_ref_cm2 = J_load / (p["ratio"]**2) * 1e4

    # Angular accel of screw (rad/s²) to create linear accel
    alpha = p["accel"] * 2*math.pi / lead_m

    # Torques (motor side)
    T_acc_motor = (J_load * alpha) / (p["ratio"] * p["eff"])
    T_drag_motor = p["drag_nom_nm"] / (p["ratio"] * p["eff"])
    Tg_motor = 0.0
    if p["vertical"]:
        Tg = (M * 9.81 * lead_m) / (2*math.pi*p["screw_eta"])  # gravity torque at screw
        Tg_motor = Tg / (p["ratio"] * p["eff"])

    T_peak = T_drag_motor + T_acc_motor + Tg_motor
    T_rms = T_drag_motor + 0.5*T_acc_motor + Tg_motor

    I_rms = T_rms / p["Kt"]
    I_peak = T_peak / p["Kt"]

    # Speeds
    n_screw = p["vmax"] / lead_m * 60.0
    n_motor = n_screw * p["ratio"]

    # Back-EMF and bus margin
    V_emf = p["Ke"] * (n_motor/1000.0)
    V_margin = p["bus_vdc"] - V_emf

    # Backlash linear
    theta = (p["backlash_arcmin"]/60.0) * math.pi/180.0  # rad
    backlash_um = (theta/(2*math.pi)) * p["lead_mm"] * 1000.0

    return dict(
        mass=M, J_load=J_load, J_ref_cm2=J_ref_cm2, alpha=alpha,
        T_acc=T_acc_motor, T_drag=T_drag_motor, Tg=Tg_motor,
        T_peak=T_peak, T_rms=T_rms, I_rms=I_rms, I_peak=I_peak,
        n_screw=n_screw, n_motor=n_motor, V_emf=V_emf, V_margin=V_margin,
        backlash_um=backlash_um
    )

def trapezoid_times(distance_m, vmax, accel):
    """Return (ta, tc, td) for a standard trapezoid or triangle profile."""
    ta = vmax / accel
    xa = 0.5*accel*ta**2
    if 2*xa >= distance_m:  # triangle
        ta = math.sqrt(distance_m/accel)
        return ta, 0.0, ta
    xc = distance_m - 2*xa
    tc = xc / vmax
    return ta, tc, ta
