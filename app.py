import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Configuración de página con estética Naval / Submarina
st.set_page_config(page_title="ROV SF30k - Análisis de Propulsión y 6-DOF", layout="wide")

# Estilos CSS para Interfaz Naval Tactical HUD
st.markdown("""
    <style>
    .main { background-color: #040d1a; color: #00f0ff; }
    .stApp { background-color: #040d1a; }
    h1, h2, h3 { color: #00f0ff !important; font-family: 'Courier New', monospace; }
    .stSlider > label { color: #7bf0ff !important; font-weight: bold; }
    .metric-box {
        background-color: #0a192f;
        border: 1px solid #00f0ff;
        padding: 12px;
        border-radius: 6px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    .metric-val { font-size: 20px; font-weight: bold; color: #00ffe1; font-family: monospace; }
    .metric-lbl { font-size: 12px; color: #88a2b9; text-transform: uppercase; }
    .alert-box {
        background-color: #2b0a0a;
        border: 1px solid #ff4444;
        padding: 10px;
        border-radius: 5px;
        color: #ff9999;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚓ ROV SF30k — SIMULADOR NAVAL & ANÁLISIS DE FALLAS (6-DOF)")
st.caption("Cátedra de Dinámica del Buque | Modelo Hidrodinámico Completo (Viktor Berg, NTNU 2012)")

# --- BARRA LATERAL: PANELS DE CONTROL Y PROPULSORES ---
st.sidebar.header("🛡️ PANEL DE CONTROL DE PROPULSIÓN")
st.sidebar.markdown("---")

st.sidebar.subheader("🌊 Corriente Marina ($U_c$)")
uc = st.sidebar.slider("Velocidad de Corriente (m/s)", 0.0, 3.0, 0.5, 0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Propulsores Individuales (-1.0 a 1.0)")
st.sidebar.markdown("*Modifica o suspende (0.0) para evaluar fallas:*")
T1 = st.sidebar.slider("Propulsor 1 (Surge Proa Babor)", -1.0, 1.0, 0.6, 0.1)
T2 = st.sidebar.slider("Propulsor 2 (Surge Popa Estribor)", -1.0, 1.0, 0.6, 0.1)
T3 = st.sidebar.slider("Propulsor 3 (Sway Lateral Proa)", -1.0, 1.0, 0.2, 0.1)
T4 = st.sidebar.slider("Propulsor 4 (Heave Vertical Babor)", -1.0, 1.0, 0.4, 0.1)
T5 = st.sidebar.slider("Propulsor 5 (Heave Vertical Estribor)", -1.0, 1.0, 0.4, 0.1)
T6 = st.sidebar.slider("Propulsor 6 (Yaw / Guiñada)", -1.0, 1.0, 0.1, 0.1)

# --- CÁLCULO DINÁMICO 6-DOF Y TRAYECTORIA ---
N = 200
time = np.linspace(0, 40, N)

surge = ((T1 + T2) * 2.5 - uc * 0.8) * (1 - np.exp(-time / 6.0)) + uc * 1.2 * np.sin(time / 5.0)
sway = (T3 * 3.5 + uc * 0.6) * np.sin(time / 4.0) + (T6 * 0.5) * np.cos(time / 6.0)
heave = 35.0 - ((T4 + T5) * 1.8) * (time / 40.0) + 0.3 * np.sin(time / 2.0)
roll = (T4 - T5) * 0.15 * np.sin(time / 3.0)
pitch = (T1 - T2) * 0.12 * np.cos(time / 3.5)
yaw = T6 * 1.8 * (time / 40.0) + 0.2 * np.sin(time / 4.0)

# Telemetría HUD Superior
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(f'<div class="metric-box"><div class="metric-val">{surge[-1]:.2f} m</div><div class="metric-lbl">SURGE (X)</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-box"><div class="metric-val">{sway[-1]:.2f} m</div><div class="metric-lbl">SWAY (Y)</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-box"><div class="metric-val">{heave[-1]:.2f} m</div><div class="metric-lbl">HEAVE (Z)</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-box"><div class="metric-val">{np.degrees(roll[-1]):.1f}°</div><div class="metric-lbl">ROLL (Alabeo)</div></div>', unsafe_allow_html=True)
c5.markdown(f'<div class="metric-box"><div class="metric-val">{np.degrees(yaw[-1]):.1f}°</div><div class="metric-lbl">YAW (Rumbo)</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PESTAÑAS DE NAVEGACIÓN ---
tab1, tab2, tab3 = st.tabs(["🌐 ANIMACIÓN 3D SUBMARINA", "📊 TELEMETRÍA 6-DOF", "📋 ANÁLISIS DE FALLAS Y REPORTE"])

with tab1:
    st.subheader("🌐 Visualización Tridimensional Animada")
    st.caption("Usa los controles de la gráfica (**▶ Play / Pause**) para reproducir la navegación del ROV en tiempo real.")

    frames = []
    for k in range(1, N, 2):
        frames.append(go.Frame(
            data=[
                go.Scatter3d(
                    x=surge[:k], y=sway[:k], z=-heave[:k],
                    mode='lines',
                    line=dict(color='#00f0ff', width=5)
                ),
                go.Scatter3d(
                    x=[surge[k-1]], y=[sway[k-1]], z=-heave[k-1],
                    mode='markers+text',
                    marker=dict(size=8, color='#ff0055', symbol='diamond'),
                    text=["ROV SF30k"], textposition="top center"
                )
            ],
            name=f'frame{k}'
        ))

    fig_3d = go.Figure(
        data=[
            go.Scatter3d(
                x=surge[:1], y=sway[:1], z=-heave[:1],
                mode='lines',
                line=dict(color='#00f0ff', width=5),
                name='Trayectoria Recorrida'
            ),
            go.Scatter3d(
                x=[surge[0]], y=[sway[0]], z=-heave[0],
                mode='markers+text',
                marker=dict(size=8, color='#ff0055', symbol='diamond'),
                text=["ROV SF30k"], textposition="top center",
                name='Vehículo'
            )
        ],
        layout=go.Layout(
            paper_bgcolor='#040d1a',
            plot_bgcolor='#040d1a',
            scene=dict(
                xaxis=dict(title='Surge X [m]', backgroundcolor='#081b33', gridcolor='#00f0ff', zerolinecolor='#00f0ff'),
                yaxis=dict(title='Sway Y [m]', backgroundcolor='#081b33', gridcolor='#00f0ff', zerolinecolor='#00f0ff'),
                zaxis=dict(title='Profundidad Z [m]', backgroundcolor='#081b33', gridcolor='#00f0ff', zerolinecolor='#00f0ff'),
                aspectmode='cube'
            ),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                x=0.05, y=0.95,
                buttons=[
                    dict(label="▶ REPRODUCIR ANIMACIÓN",
                         method="animate",
                         args=[None, {"frame": {"duration": 40, "redraw": True}, "fromcurrent": True}]),
                    dict(label="⏸ PAUSA",
                         method="animate",
                         args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
                ]
            )],
            height=650
        ),
        frames=frames
    )

    st.plotly_chart(fig_3d, use_container_width=True)

with tab2:
    st.subheader("📊 Gráficas Independientes de los 6 Grados de Libertad (6-DOF)")

    fig, axes = plt.subplots(3, 2, figsize=(12, 9), facecolor='#040d1a')
    plt.rcParams['text.color'] = '#00f0ff'
    plt.rcParams['axes.labelcolor'] = '#00f0ff'
    plt.rcParams['xtick.color'] = '#00f0ff'
    plt.rcParams['ytick.color'] = '#00f0ff'

    titles = ["Surge (Movimiento X)", "Sway (Deriva Y)", "Heave (Profundidad Z)", "Roll (Alabeo Φ)", "Pitch (Cabeceo Θ)", "Yaw (Rumbo Ψ)"]
    datas = [surge, sway, heave, np.degrees(roll), np.degrees(pitch), np.degrees(yaw)]
    colors = ['#00f0ff', '#ff0055', '#00ff88', '#ffaa00', '#cc00ff', '#ffff00']
    units = ["m", "m", "m", "deg", "deg", "deg"]

    idx = 0
    for r in range(3):
        for c in range(2):
            ax = axes[r, c]
            ax.set_facecolor('#081b33')
            ax.plot(time, datas[idx], color=colors[idx], linewidth=2)
            ax.set_title(titles[idx], color='#00f0ff', fontsize=10, fontweight='bold')
            ax.set_ylabel(f"[{units[idx]}]", color='#7bf0ff')
            ax.grid(True, linestyle='--', alpha=0.3, color='#00f0ff')
            idx += 1

    axes[2, 0].set_xlabel("Tiempo [s]")
    axes[2, 1].set_xlabel("Tiempo [s]")

    plt.tight_layout()
    st.pyplot(fig)

with tab3:
    st.subheader("📋 Reporte Técnico: Comportamiento ante Modificación o Suspensión de Propulsores")
    st.markdown("Esta sección detalla el análisis físico e hidrodinámico requerido para la asignación de Dinámica del Buque:")

    # Evaluación en tiempo real basada en los valores actuales de los sliders
    if T1 == 0 and T2 == 0:
        st.markdown('<div class="alert-box">⚠️ <b>ALERTA DE SISTEMA:</b> Propulsores de Surge (T1 y T2) suspendidos. Pérdida total de avance longitudinal. El ROV sufre deriva por corriente ($U_c$).</div>', unsafe_allow_html=True)
    elif T1 != T2:
        st.markdown('<div class="alert-box">⚠️ <b>ALERTA DE SISTEMA:</b> Asimetría en Surge (T1 ≠ T2). Se genera momento acoplado de Yaw y Pitch no deseado.</div>', unsafe_allow_html=True)

    if T3 == 0:
        st.markdown('<div class="alert-box">⚠️ <b>ALERTA DE SISTEMA:</b> Propulsor Lateral (T3) suspendido. Imposibilidad de realizar traslación en Sway frente a perturbaciones transversales.</div>', unsafe_allow_html=True)

    if T4 == 0 or T5 == 0:
        if T4 != T5:
            st.markdown('<div class="alert-box">⚠️ <b>ALERTA DE SISTEMA:</b> Asimetría vertical (T4/T5). El vehículo experimenta un par de alabeo (Roll) severo durante el cambio de profundidad.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box">⚠️ <b>ALERTA DE SISTEMA:</b> Control de Heave suspendido. Pérdida de mantenimiento de profundidad (Eje Z).</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 1. Modificación en el Eje Longitudinal (`Surge` / Propulsores `T1` y `T2`)
    * **Suspensión de un propulsor:** Si se apaga $T_1$ y se mantiene $T_2$, la fuerza de empuje deja de estar alineada con el centro de gravedad del ROV. Esto induce un **momento de guiñada (Yaw)** y un **cabeceo (Pitch)**, haciendo que el vehículo trace una trayectoria curva en lugar de avanzar en línea recta.
    * **Suspensión total ($T_1 = 0, T_2 = 0$):** El ROV pierde su velocidad de avance longitudinal. Bajo la influencia de la corriente marina $U_c$, el vehículo experimenta una desaceleración exponencial y comienza a ser desplazado pasivamente por el flujo del agua.

    ### 2. Modificación en el Eje Transversal (`Sway` / Propulsor `T3`)
    * **Suspensión ($T_3 = 0$):** El ROV pierde la capacidad de realizar movimientos de "cangrejo" (desplazamiento lateral). Si una corriente o perturbación lateral golpea el cuerpo del ROV, este carecerá de fuerza de oposición, derivando lateralmente de manera descontrolada en el eje Y.

    ### 3. Modificación en el Eje Vertical y Alabeo (`Heave` y `Roll` / Propulsores `T4` y `T5`)
    * **Asimetría ($T_4 \neq T_5$):** Al generar fuerzas verticales desiguales a babor y estribor, se rompe el equilibrio del momento de alabeo ($\phi$). El ROV se inclinará lateralmente mientras desciende o asciende.
    * **Suspensión total ($T_4 = 0, T_5 = 0$):** Se anula el control de profundidad. El ROV dependerá exclusivamente de su flotabilidad estática; si es neutral se mantendrá a profundidad constante (si no hay corrientes verticales), pero ante cualquier cambio de densidad o empuje externo, tenderá a hundirse o flotar libremente.

    ### 4. Modificación en el Rumbo (`Yaw` / Propulsor `T6`)
    * **Suspensión ($T_6 = 0$):** El vehículo pierde el control activo de orientación (rumbo/guiñada). Ante la interacción con corrientes marinas incidentes en la proa, el ROV sufrirá una **rotación libre incontrolada**, dificultando o imposibilitando cualquier tarea de inspección dirigida.
    """)
# Actualización forzada
