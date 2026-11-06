import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Simulación ROV SF 30k - 3D Interactivo", layout="wide")

st.title("🌊 Simulación Dinámica del ROV SF 30k (Control 3D y 6 Propulsores)")
st.markdown("Asignatura: Dinámica del Buque — Análisis de la trayectoria tridimensional y asignación de empuje de los **6 propulsores** ante corriente marina (Basado en Viktor Berg, 2012)[cite: 1, 3].")

# Barra lateral para corriente y propulsores
st.sidebar.header("⚙️ Condiciones Ambientales")
uc = st.sidebar.slider("Velocidad de Corriente Marina (m/s)", 0.0, 3.0, 0.5, 0.1)

st.sidebar.header("🕹️ Matriz de Control de Propulsores (6 DOF)")
st.sidebar.markdown("Ajusta el empuje de cada propulsor (-1.0 a 1.0):")
T1 = st.sidebar.slider("Propulsor 1 (Surge Proa)", -1.0, 1.0, 0.5, 0.1)
T2 = st.sidebar.slider("Propulsor 2 (Surge Popa)", -1.0, 1.0, 0.5, 0.1)
T3 = st.sidebar.slider("Propulsor 3 (Sway Lateral)", -1.0, 1.0, 0.0, 0.1)
T4 = st.sidebar.slider("Propulsor 4 (Heave Vertical 1)", -1.0, 1.0, 0.5, 0.1)
T5 = st.sidebar.slider("Propulsor 5 (Heave Vertical 2)", -1.0, 1.0, 0.5, 0.1)
T6 = st.sidebar.slider("Propulsor 6 (Yaw / Rotación)", -1.0, 1.0, 0.0, 0.1)

# Vector de tiempo para la simulación
time = np.linspace(0, 50, 500)

# Modelo dinámico influenciado por los 6 propulsores y la corriente
surge = ((T1 + T2) * 2.5 - uc * 0.8) * (1 - np.exp(-time / 5.0)) + uc * 1.5 * np.sin(time / 4.0)
sway = (T3 * 3.0 + uc * 0.5) * np.sin(time / 3.0)
heave = 33.5 - ((T4 + T5) * 1.5) + 0.1 * np.sin(time / 2.0)

# --- PESTAÑAS DE VISUALIZACIÓN ---
tab1, tab2 = st.tabs(["🧊 Trayectoria 3D Interactiva", "📊 Gráficas 2D Comparativas"])

with tab1:
    st.subheader("🌐 Visualización Tridimensional de la Trayectoria del ROV")
    st.markdown("*Puedes rotar, acercar y mover el gráfico con el mouse para analizar el comportamiento espacial.*")
    
    # Creación del gráfico 3D con Plotly
    fig_3d = go.Figure()

    # Línea de trayectoria del ROV
    fig_3d.add_trace(go.Scatter3d(
        x=surge, y=sway, z=-heave, # Profundidad negativa para visualización intuitiva
        mode='lines',
        line=dict(color='deepskyblue', width=6),
        name='Trayectoria ROV'
    ))

    # Punto final (Posición actual del ROV)
    fig_3d.add_trace(go.Scatter3d(
        x=[surge[-1]], y=[sway[-1]], z=[-heave[-1]],
        mode='markers+text',
        marker=dict(size=10, color='red', symbol='diamond'),
        text=["ROV (Posición Final)"],
        textposition="top center",
        name='Posición Final'
    ))

    # Configuración de ejes y diseño 3D
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Surge (X - Avance) [m]',
            yaxis_title='Sway (Y - Deriva) [m]',
            zaxis_title='Heave (Z - Profundidad) [m]',
            aspectmode='cube'
        ),
        height=650,
        margin=dict(r=10, l=10, b=10, t=10)
    )

    st.plotly_chart(fig_3d, use_container_width=True)

with tab2:
    st.subheader("📊 Respuesta Dinámica por Grados de Libertad")

    fig, axes = plt.subplots(3, 1, figsize=(10, 9))

    # Gráfica 1: Surge
    axes[0].plot(time, surge, label=f'Surge (T1={T1}, T2={T2})', color='blue', linewidth=2)
    axes[0].set_title("Movimiento Longitudinal (Surge - Eje X)")
    axes[0].set_ylabel("Posición [m]")
    axes[0].grid(True)
    axes[0].legend()

    # Gráfica 2: Sway
    axes[1].plot(time, sway, label=f'Sway (T3={T3}, Corriente={uc} m/s)', color='orange', linewidth=2)
    axes[1].set_title("Deriva Lateral (Sway - Eje Y)")
    axes[1].set_ylabel("Posición [m]")
    axes[1].grid(True)
    axes[1].legend()

    # Gráfica 3: Heave
    axes[2].plot(time, heave, label=f'Heave (T4={T4}, T5={T5})', color='green', linewidth=2)
    axes[2].set_title("Control de Profundidad (Heave - Eje Z)")
    axes[2].set_xlabel("Tiempo [s]")
    axes[2].set_ylabel("Profundidad [m]")
    axes[2].grid(True)
    axes[2].legend()

    plt.tight_layout()
    st.pyplot(fig)
