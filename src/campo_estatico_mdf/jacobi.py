# src/campo_estatico_mdf/jacobi.py
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from .bc import impose_dirichlet

@dataclass
class ConvergenceInfo:
    """
    Registro ligero con la información de convergencia de un método iterativo.

    Attributes
    ----------
    iterations : int
        Número total de iteraciones realizadas.
    max_diff : float
        Máxima diferencia absoluta entre iteraciones consecutivas al finalizar.
    tol : float
        Tolerancia utilizada como criterio de parada.
    """
    iterations: int
    max_diff: float
    tol: float


def jacobi_solve(
    V0: np.ndarray,
    left, right, top, bottom,
    tol: float = 1e-5,
    max_iter: int = 10000,
) -> tuple[np.ndarray, ConvergenceInfo]:
    """
    Resuelve la ecuación de Laplace :math:`\\nabla^2 V = 0` en una malla cuadrada
    mediante el método iterativo de Jacobi con condiciones de frontera de Dirichlet.

    **Resumen del método**

    El método de Jacobi actualiza cada nodo interior mediante el promedio aritmético
    de sus cuatro vecinos más cercanos:

    .. math::

        V^{(n+1)}_{i,j} =
        \\tfrac{1}{4} \\left(
        V^{(n)}_{i+1,j} +
        V^{(n)}_{i-1,j} +
        V^{(n)}_{i,j+1} +
        V^{(n)}_{i,j-1}
        \\right).

    El proceso continúa hasta que la norma infinito de la diferencia entre iteraciones
    consecutivas sea menor que ``tol`` o hasta agotar ``max_iter``.

    Parameters
    ----------
    V0 : numpy.ndarray of shape (N, N)
        Potencial inicial.  
        Solo se actualizan los nodos interiores; los valores en las fronteras se
        reimponen en cada iteración.
    left, right, top, bottom : float or array_like
        Valores de frontera sobre los bordes izquierdo, derecho, superior e inferior,
        respectivamente.  
        Se aceptan escalares o arreglos compatibles con la dimensión del borde.
    tol : float, default=1e-5
        Criterio de convergencia basado en la máxima diferencia absoluta entre
        iteraciones.
    max_iter : int, default=10000
        Número máximo de iteraciones permitidas.

    Returns
    -------
    V : numpy.ndarray
        Distribución del potencial tras completar el método iterativo, incluyendo
        las condiciones de frontera.
    info : ConvergenceInfo
        Información sobre la convergencia del algoritmo: número de iteraciones,
        último valor de ``max_diff`` y tolerancia aplicada.

    Notes
    -----
    La convergencia del método de Jacobi está garantizada para operadores diagonales
    dominantes como el Laplaciano discreto en 2D con condiciones de Dirichlet.

    References
    ----------
    - Método de Jacobi para sistemas lineales.
    """
    V = V0.copy()
    impose_dirichlet(V, left, right, top, bottom)
    N = V.shape[0]

    for k in range(1, max_iter + 1):
        Vn = V.copy()

        # Actualización Jacobi (solo nodos interiores)
        Vn[1:-1, 1:-1] = 0.25 * (
            V[1:-1, 2:] + V[1:-1, :-2] +
            V[2:, 1:-1] + V[:-2, 1:-1]
        )

        impose_dirichlet(Vn, left, right, top, bottom)

        diff = float(np.max(np.abs(Vn - V)))
        V = Vn

        if diff < tol:
            return V, ConvergenceInfo(k, diff, float(tol))

    return V, ConvergenceInfo(max_iter, diff, float(tol))
