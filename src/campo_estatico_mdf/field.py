# src/campo_estatico_mdf/field.py
from __future__ import annotations
import numpy as np

def electric_field(V, h: float = 1.0):
    """
    Calcula el campo eléctrico :math:`\\mathbf{E} = -\\nabla V` en una malla cartesiana uniforme.

    El gradiente del potencial se evalúa mediante diferencias centrales utilizando
    ``numpy.gradient``.  
    Recordando que en electrostática el campo eléctrico se define como:

    .. math::

        \\mathbf{E} = -\\nabla V = -\\left( \\frac{\\partial V}{\\partial x},
        \\frac{\\partial V}{\\partial y} \\right),

    se devuelve la pareja de matrices ``(Ex, Ey)`` con las componentes en las
    direcciones ``x`` y ``y``, respectivamente.

    Parameters
    ----------
    V : numpy.ndarray of shape (N, N)
        Matriz del potencial eléctrico evaluado en los nodos de la malla.
        Se asume el convenio de indexación ``V[y, x]``.
    h : float, default=1.0
        Separación uniforme entre puntos de la malla (``Δx = Δy = h``).

    Returns
    -------
    Ex : numpy.ndarray
        Componente del campo eléctrico en la dirección ``x``, misma forma que ``V``.
    Ey : numpy.ndarray
        Componente del campo eléctrico en la dirección ``y``, misma forma que ``V``.

    Notes
    -----
    ``numpy.gradient`` retorna ``(dV/dy, dV/dx)``.  
    Se aplica el signo negativo al gradiente para obtener el campo eléctrico de acuerdo
    con la convención electrostática estándar.
    """
    gy, gx = np.gradient(V, h, h, edge_order=2)  # dV/dy, dV/dx
    return -gx, -gy
