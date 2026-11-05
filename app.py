import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulación ROV SF 30k", layout="wide")

st.title("🌊 Simulación Dinámica del ROV SF 30k")
st.markdown("Tarea de Dinámica del Buque — Análisis del comportamiento ante corriente marina (Basado en Viktor Berg, 2012).")

# Barra lateral para modificar las 3 condiciones de corriente marina exigidas
st.sidebar.header("⚙️ Configuración de Corriente")
uc1 = st.sidebar.slider("Velocidad de Corriente - Condición 1 (m/s)", 0.0, 0.5, 0.1, 0.05)
uc2 = st.sidebar.slider("Velocidad de Corriente - Condición 2 (m/s)", 0.5, 1.5, 0.8, 0.05)
uc3 = st.sidebar.slider("Velocidad de Corriente - Condición 3 (m/s)", 1.5, 3.0, 2.0, 0.05)

# Vector de tiempo para la simulación
time = np.linspace(0, 50, 500)

def simular_rov(uc):
    # Modelo dinámico simplificado del ROV SF 30k (Surge, Sway, Heave)
    surge = (2.0 - uc * 0.8) * (1 - np.exp(-time / 5.0)) + uc * 2.0 * np.sin(time / 4.0)
    sway = uc * 0.5 * np.sin(time / 3.0)
    heave = 33.5 + 0.1 * np.sin(time / 2.0)
    return time, surge, sway, heave

# Ejecución para las 3 condiciones
t, s1, sw1, h1 = simular_rov(uc1)
_, s2, sw2, h2 = simular_rov(uc2)
_, s3, sw3, h3 = simular_rov(uc3)

# Visualización de Gráficas Comparativas
st.subheader("📊 Gráficas Comparativas de Movimiento del ROV")

fig, axes = plt.subplots(3, 1, figsize=(10, 9))

# Gráfica 1: Surge (Eje X)
axes[0].plot(t, s1, label=f'Condición 1 ({uc1} m/s)', color='blue', linewidth=2)
axes[0].plot(t, s2, label=f'Condición 2 ({uc2} m/s)', color='orange', linewidth=2)
axes[0].plot(t, s3, label=f'Condición 3 ({uc3} m/s)', color='red', linewidth=2)
axes[0].set_title("Movimiento Longitudinal (Surge - Eje X)")
axes[0].set_ylabel("Posición [m]")
axes[0].grid(True)
axes[0].legend()

# Gráfica 2: Sway (Eje Y)
axes[1].plot(t, sw1, label=f'Condición 1 ({uc1} m/s)', color='blue', linewidth=2)
axes[1].plot(t, sw2, label=f'Condición 2 ({uc2} m/s)', color='orange', linewidth=2)
axes[1].plot(t, sw3, label=f'Condición 3 ({uc3} m/s)', color='red', linewidth=2)
axes[1].set_title("Deriva Lateral (Sway - Eje Y)")
axes[1].set_ylabel("Posición [m]")
axes[1].grid(True)
axes[1].legend()

# Gráfica 3: Heave (Eje Z)
axes[2].plot(t, h1, label=f'Condición 1 ({uc1} m/s)', color='blue', linewidth=2)
axes[2].plot(t, h2, label=f'Condición 2 ({uc2} m/s)', color='orange', linewidth=2)
axes[2].plot(t, h3, label=f'Condición 3 ({uc3} m/s)', color='red', linewidth=2)
axes[2].set_title("Control de Profundidad (Heave - Eje Z)")
axes[2].set_xlabel("Tiempo [s]")
axes[2].set_ylabel("Profundidad [m]")
axes[2].grid(True)
axes[2].legend()

plt.tight_layout()
st.pyplot(fig)
