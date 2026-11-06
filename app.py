import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Configuración de página con estética Naval / Submarina
st.set_page_config(page_title="ROV SF30k - Naval Subsea HUD", layout="wide")

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
    </style>
""", unsafe_allow_html=True)

st.title("⚓ ROV SF30k — SIMULADOR NAVAL 6-DOF (HUD)")
st.caption("Cátedra de Dinámica del Buque | Modelo Hidrodinámico Completo (Viktor Berg, NTNU 2012)")

# --- BARRA LATERAL: PANELS DE CONTROL Y PROPULSORES ---
st.sidebar.header("🛡️ PANEL DE CONTROL DE PROPULSIÓN")
st.sidebar.markdown("---")

st.sidebar.subheader("🌊 Corriente Marina ($U_c$)")
uc = st.sidebar.slider("Velocidad de Corriente (m/s)", 0.0, 3.0, 0.5, 0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Propulsores Individuales (-1.0 a 1.0)")
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
tab1, tab2 = st.tabs(["🌐 ANIMACIÓN TRAYECTORIA 3D SUBMARINA", "📊 TELEMETRÍA DINÁMICA 6-DOF"])

with tab1:
    st.subheader("🌐 Visualización Tridimensional Animada (Plotly Frames)")
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
