# src/campo_estatico_mdf/visual.py
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from .field import electric_field

def plot_potential(V: np.ndarray, cmap: str = "viridis", figsize=(6, 5)) -> plt.Figure:
    """
    Grafica un heatmap del potencial eléctrico V.

    Parameters
    ----------
    V : np.ndarray
        Matriz del potencial eléctrico.
    cmap : str, default="viridis"
        Colormap para la visualización.
    figsize : tuple (ancho, alto), default=(6,5)
        Tamaño de la figura en pulgadas.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figura lista para mostrar en Streamlit o matplotlib.
    """
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(V, origin="lower", cmap=cmap, interpolation="nearest")
    ax.set_title("Potencial eléctrico V(x, y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig.colorbar(im, ax=ax, label="V")
    return fig

def plot_field(V: np.ndarray, h: float = 1.0, stride: int = 1, figsize=(6, 5)) -> plt.Figure:
    """
    Grafica el campo eléctrico como quiver plot sobre la malla.

    Parameters
    ----------
    V : np.ndarray
        Matriz del potencial eléctrico.
    h : float, default=1.0
        Paso de la malla (Δx = Δy = h).
    stride : int, default=1
        Intervalo para mostrar vectores, útil para no saturar la figura.
    figsize : tuple (ancho, alto), default=(6,5)
        Tamaño de la figura en pulgadas.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figura lista para mostrar en Streamlit o matplotlib.
    """
    Ex, Ey = electric_field(V, h)
    Y, X = np.meshgrid(np.arange(0, V.shape[0]), np.arange(0, V.shape[1]), indexing="ij")

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(V, origin="lower", cmap="viridis", interpolation="nearest", alpha=0.6)
    ax.quiver(
        X[::stride, ::stride], Y[::stride, ::stride],
        Ex[::stride, ::stride], Ey[::stride, ::stride],
        color="red", scale=50
    )
    ax.set_title("Campo eléctrico y potencial")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig
