# src/campo_estatico_mdf/grid.py
from __future__ import annotations
import numpy as np

def allocate_potential(N: int, h: float = 1.0) -> tuple[np.ndarray, float]:
    """
    Crea y asigna una malla cuadrada para el potencial eléctrico.

    Esta función construye una matriz ``V`` de tamaño ``(N, N)`` que representa
    la discretización uniforme de una región cuadrada en 2D, con un paso espacial
    ``h`` en las direcciones ``x`` y ``y``.  
    La malla se usa típicamente con el esquema de diferencias finitas de cinco puntos
    para resolver la ecuación de Laplace:

    .. math::

        V_{i+1,j} + V_{i-1,j} + V_{i,j+1} + V_{i,j-1} - 4V_{i,j} = 0

    para todos los nodos interiores.

    Parameters
    ----------
    N : int
        Número de puntos por dimensión en la malla.  
        Debe ser ``>= 3`` para garantizar que exista al menos un nodo interior.
    h : float, default=1.0
        Paso espacial en ambas direcciones (``Δx = Δy = h``).

    Returns
    -------
    V : numpy.ndarray of shape (N, N)
        Matriz del potencial inicializada en ceros.  
        Las condiciones de frontera deben aplicarse mediante
        :func:`campo_estatico_mdf.bc.impose_dirichlet`.
    h : float
        Valor del paso espacial, útil para gradientes y cálculo del campo eléctrico.

    See Also
    --------
    campo_estatico_mdf.bc.impose_dirichlet :
        Función para imponer condiciones de contorno de Dirichlet.
    """
    if N < 3:
        raise ValueError("N debe ser >= 3 para que exista un interior válido.")
    return np.zeros((int(N), int(N)), dtype=float), float(h)
