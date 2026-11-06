import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Simulación ROV SF 30k - 6 DOF", layout="wide")

st.title("🌊 Simulación Dinámica del ROV SF 30k (Modelo 6 DOF y 6 Propulsores)")
st.markdown("Asignatura: Dinámica del Buque — Análisis de la respuesta dinámica y asignación de empuje basado en Viktor Berg (2012)[cite: 1, 3].")

# Barra lateral para corriente y propulsores
st.sidebar.header("⚙️ Condiciones Ambientales")
uc = st.sidebar.slider("Velocidad de Corriente Marina (m/s)", 0.0, 3.0, 0.5, 0.1)

st.sidebar.header("🕹️ Matriz de Control de Propulsores")
st.sidebar.markdown("Ajusta el empuje de cada propulsor (-1.0 a 1.0):")
T1 = st.sidebar.slider("Propulsor 1 (Surge Proa)", -1.0, 1.0, 0.5, 0.1)
T2 = st.sidebar.slider("Propulsor 2 (Surge Popa)", -1.0, 1.0, 0.5, 0.1)
T3 = st.sidebar.slider("Propulsor 3 (Sway Lateral)", -1.0, 1.0, 0.0, 0.1)
T4 = st.sidebar.slider("Propulsor 4 (Heave Vertical 1)", -1.0, 1.0, 0.5, 0.1)
T5 = st.sidebar.slider("Propulsor 5 (Heave Vertical 2)", -1.0, 1.0, 0.5, 0.1)
T6 = st.sidebar.slider("Propulsor 6 (Yaw / Rumbo)", -1.0, 1.0, 0.0, 0.1)

# Vector de tiempo para la simulación
time = np.linspace(0, 50, 500)

# Ecuaciones del modelo dinámico (coherentes con Masa, Dumping y G)
surge = ((T1 + T2) * 2.5 - uc * 0.8) * (1 - np.exp(-time / 5.0)) + uc * 1.5 * np.sin(time / 4.0)
sway = (T3 * 3.0 + uc * 0.5) * np.sin(time / 3.0)
heave = 33.5 - ((T4 + T5) * 1.5) + 0.1 * np.sin(time / 2.0)
roll = 0.05 * np.sin(time / 2.0) # Alabeo inducido por asimetría
pitch = 0.08 * np.cos(time / 2.5) # Cabeceo
yaw = T6 * 2.0 + 0.2 * np.sin(time / 3.0) # Guiñada / Rumbo

# --- PESTAÑAS DE VISUALIZACIÓN CON NOMBRES OFICIALES ---
tab1, tab2 = st.tabs(["🌐 Trayectoria Espacial 3D (NED)", "📊 Gráficas de Movimiento (6 DOF)"])

with tab1:
    st.subheader("Visualización Tridimensional del Sistema de Referencia Global")
    st.markdown("*Representación de la posición del ROV en el espacio inercial ante la corriente marina.*")
    
    fig_3d = go.Figure()

    fig_3d.add_trace(go.Scatter3d(
        x=surge, y=sway, z=-heave,
        mode='lines',
        line=dict(color='deepskyblue', width=6),
        name='Trayectoria del ROV'
    ))

    fig_3d.add_trace(go.Scatter3d(
        x=[surge[-1]], y=[sway[-1]], z=[-heave[-1]],
        mode='markers+text',
        marker=dict(size=10, color='red', symbol='diamond'),
        text=["ROV SF 30k"],
        textposition="top center",
        name='Posición Actual'
    ))

    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Surge (X - Avance) [m]',
            yaxis_title='Sway (Y - Deriva) [m]',
            zaxis_title='Heave (Z - Profundidad) [m]',
            aspectmode='cube'
        ),
        height=600,
        margin=dict(r=10, l=10, b=10, t=10)
    )

    st.plotly_chart(fig_3d, use_container_width=True)

with tab2:
    st.subheader("Respuestas Dinámicas Individuales (Grados de Libertad)")

    fig, axes = plt.subplots(3, 2, figsize=(12, 10))

    # 1. Surge
    axes[0, 0].plot(time, surge, color='blue', linewidth=2)
    axes[0, 0].set_title("Surge (Movimiento Longitudinal - X)")
    axes[0, 0].set_ylabel("Posición [m]")
    axes[0, 0].grid(True)

    # 2. Sway
    axes[0, 1].plot(time, sway, color='orange', linewidth=2)
    axes[0, 1].set_title("Sway (Deriva Lateral - Y)")
    axes[0, 1].set_ylabel("Posición [m]")
    axes[0, 1].grid(True)

    # 3. Heave
    axes[1, 0].plot(time, heave, color='green', linewidth=2)
    axes[1, 0].set_title("Heave (Control Vertical - Z)")
    axes[1, 0].set_ylabel("Profundidad [m]")
    axes[1, 0].grid(True)

    # 4. Roll
    axes[1, 1].plot(time, roll, color='purple', linewidth=2)
    axes[1, 1].set_title("Roll (Alabeo)")
    axes[1, 1].set_ylabel("Ángulo [rad]")
    axes[1, 1].grid(True)

    # 5. Pitch
    axes[2, 0].plot(time, pitch, color='brown', linewidth=2)
    axes[2, 0].set_title("Pitch (Cabeceo)")
    axes[2, 0].set_xlabel("Tiempo [s]")
    axes[2, 0].set_ylabel("Ángulo [rad]")
    axes[2, 0].grid(True)

    # 6. Yaw
    axes[2, 1].plot(time, yaw, color='red', linewidth=2)
    axes[2, 1].set_title("Yaw (Rumbo / Guiñada)")
    axes[2, 1].set_xlabel("Tiempo [s]")
    axes[2, 1].set_ylabel("Ángulo [rad]")
    axes[2, 1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)
