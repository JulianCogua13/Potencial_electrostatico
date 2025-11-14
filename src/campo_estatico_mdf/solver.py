# src/campo_estatico_mdf/solver.py
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .grid import allocate_potential
from .bc import edge_to_array, impose_dirichlet
from .jacobi import jacobi_solve, ConvergenceInfo
from .field import electric_field

@dataclass
class BoundarySpec:
    """
    Contenedor para las cuatro fronteras de Dirichlet de la malla.

    Attributes
    ----------
    left : numpy.ndarray
        Valores del borde izquierdo (longitud N).
    right : numpy.ndarray
        Valores del borde derecho (longitud N).
    top : numpy.ndarray
        Valores del borde superior (longitud N).
    bottom : numpy.ndarray
        Valores del borde inferior (longitud N).
    """
    left: np.ndarray
    right: np.ndarray
    top: np.ndarray
    bottom: np.ndarray


class LaplaceSolver2D:
    """
    Interfaz de alto nivel para resolver la ecuación de Laplace en 2D sobre una
    malla cuadrada mediante el método de Jacobi.

    Esta clase integra los distintos módulos del paquete:

    - :mod:`grid` para la creación de la malla del potencial,
    - :mod:`bc` para la gestión de las condiciones de frontera,
    - :mod:`jacobi` para la resolución iterativa de :math:`\\nabla^2 V = 0`,
    - :mod:`field` para calcular el campo eléctrico :math:`\\mathbf{E} = -\\nabla V`.

    Parameters
    ----------
    N : int
        Tamaño de la malla en cada dimensión (la malla es de ``N × N``).
    left, right, top, bottom : float or array_like
        Valores de Dirichlet para cada borde de la región.
        Pueden ser escalares (frontera uniforme) o arreglos de longitud ``N``.
    h : float, default=1.0
        Tamaño de paso espacial (``Δx = Δy = h``).

    Attributes
    ----------
    V : numpy.ndarray
        Matriz del potencial incluyendo las condiciones de frontera.
    h : float
        Paso espacial asociado a la malla.
    boundary : BoundarySpec
        Estructura que contiene las cuatro fronteras normalizadas.
    info : ConvergenceInfo
        Información de convergencia del último llamado al método de solución.

    Notes
    -----
    Las actualizaciones del interior de la malla siguen el esquema clásico
    de 5 puntos del Laplaciano discreto en 2D.
    """

    def __init__(self, N: int, left=0.0, right=0.0, top=0.0, bottom=0.0, h: float = 1.0):
        self.N = int(N)
        self.V, self.h = allocate_potential(self.N, h)
        self.boundary = self._normalize_boundaries(left, right, top, bottom)
        impose_dirichlet(
            self.V,
            self.boundary.left, self.boundary.right,
            self.boundary.top, self.boundary.bottom
        )
        self.info = ConvergenceInfo(0, float("inf"), 0.0)

    def _normalize_boundaries(self, left, right, top, bottom) -> BoundarySpec:
        """Convierte los valores de frontera en arreglos apropiados de longitud N."""
        N = self.N
        return BoundarySpec(
            edge_to_array(N, left),
            edge_to_array(N, right),
            edge_to_array(N, top),
            edge_to_array(N, bottom),
        )

    def set_boundaries(self, left=None, right=None, top=None, bottom=None):
        """
        Actualiza parcialmente o totalmente las condiciones de frontera y las
        reimpone en el potencial actual.

        Parameters
        ----------
        left, right, top, bottom : float or array_like or None
            Nuevos valores de frontera.  
            Si un parámetro es ``None``, se conserva el valor anterior.
        """
        b = self.boundary
        self.boundary = BoundarySpec(
            edge_to_array(self.N, b.left if left is None else left),
            edge_to_array(self.N, b.right if right is None else right),
            edge_to_array(self.N, b.top if top is None else top),
            edge_to_array(self.N, b.bottom if bottom is None else bottom),
        )

        impose_dirichlet(
            self.V,
            self.boundary.left, self.boundary.right,
            self.boundary.top, self.boundary.bottom
        )

    def solve_jacobi(self, tol: float = 1e-5, max_iter: int = 10000) -> ConvergenceInfo:
        """
        Ejecuta el método de Jacobi hasta que la actualización máxima sea menor
        que ``tol`` o hasta cumplir ``max_iter``.

        Parameters
        ----------
        tol : float, default=1e-5
            Tolerancia de convergencia basada en la norma infinito.
        max_iter : int, default=10000
            Número máximo de iteraciones permitidas.

        Returns
        -------
        ConvergenceInfo
            Información de la convergencia del proceso iterativo.
        """
        self.V, self.info = jacobi_solve(
            self.V,
            self.boundary.left, self.boundary.right,
            self.boundary.top, self.boundary.bottom,
            tol=tol, max_iter=max_iter
        )
        return self.info

    def electric_field(self):
        """
        Calcula y devuelve las componentes del campo eléctrico
        :math:`(E_x, E_y)` a partir del potencial actual.

        Returns
        -------
        Ex, Ey : numpy.ndarray
            Componentes del campo eléctrico con la misma forma que ``V``.
        """
        return electric_field(self.V, self.h)
