import streamlit as st
from campo_estatico_mdf.solver import LaplaceSolver2D
from campo_estatico_mdf.visual import plot_potential, plot_field

st.set_page_config(page_title="Simulación Electroestática 2D", layout="wide")
st.title("Simulación Electroestática en Región Cuadrada")

# --- Inputs del usuario (sidebar) ---
st.sidebar.header("Parámetros de simulación")
N = st.sidebar.number_input("Tamaño de la malla (N x N)", min_value=3, max_value=200, value=50, step=1)
left = st.sidebar.number_input("Voltaje borde izquierdo (V)", value=0.0)
right = st.sidebar.number_input("Voltaje borde derecho (V)", value=10.0)
top = st.sidebar.number_input("Voltaje borde superior (V)", value=5.0)
bottom = st.sidebar.number_input("Voltaje borde inferior (V)", value=0.0)
tol = st.sidebar.number_input("Tolerancia ε", min_value=1e-8, max_value=1.0, value=1e-5, format="%.1e")
stride = st.sidebar.slider("Paso para vectores (quiver)", min_value=1, max_value=10, value=2)

# --- Inputs para tamaño de las figuras ---
st.sidebar.header("Tamaño de las gráficas")
fig_width = st.sidebar.number_input("Ancho figura", min_value=4, max_value=20, value=8)
fig_height = st.sidebar.number_input("Alto figura", min_value=4, max_value=20, value=6)

run_sim = st.sidebar.button("Ejecutar simulación")

# --- Procesamiento ---
if run_sim:
    with st.spinner("Ejecutando el solver de Jacobi..."):
        solver = LaplaceSolver2D(N=N, left=left, right=right, top=top, bottom=bottom)
        info = solver.solve_jacobi(tol=tol, max_iter=10000)

    # --- Sección principal dividida en 2 columnas ---
    col_graf, col_metrics = st.columns([3, 1])  # 3:1 proporción

    with col_graf:
        st.subheader("Mapa de potencial eléctrico V(x, y)")
        fig1 = plot_potential(solver.V, figsize=(fig_width, fig_height))
        st.pyplot(fig1)

        st.subheader("Campo eléctrico E(x, y)")
        fig2 = plot_field(solver.V, solver.h, stride=stride, figsize=(fig_width, fig_height))
        st.pyplot(fig2)

    with col_metrics:
        st.subheader("Métrica de convergencia")
        st.write(f"Número de iteraciones: {info.iterations}")
        st.write(f"Diferencia máxima final: {info.max_diff:.3e}")
        st.write(f"Tolerancia usada: {info.tol:.3e}")
