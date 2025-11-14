# src/campo_estatico_mdf/bc.py
from __future__ import annotations
import numpy as np

def edge_to_array(N: int, val) -> np.ndarray:
    """
    Normaliza un valor escalar o un vector 1D para representar una condición
    de frontera en forma de un arreglo de longitud ``N``.

    Esto permite definir condiciones de Dirichlet ya sea mediante un valor
    constante en toda la frontera o mediante una distribución que varía a lo
    largo del borde.

    Parameters
    ----------
    N : int
        Número de nodos en el borde correspondiente.
    val : float or array_like
        Puede ser un valor escalar (frontera uniforme) o un arreglo de longitud ``N``
        que especifique el potencial nodo por nodo.

    Returns
    -------
    arr : numpy.ndarray of shape (N,)
        Arreglo de valores de frontera convertido a tipo flotante.

    Raises
    ------
    ValueError
        Si ``val`` es un arreglo pero su longitud no es exactamente ``N``.

    Notes
    -----
    Esta función facilita definir fronteras espacialmente uniformes o variables.
    """
    if np.isscalar(val):
        return np.full(N, float(val))

    arr = np.asarray(val, dtype=float)
    if arr.shape != (N,):
        raise ValueError("Cada frontera debe ser un escalar o un vector de longitud N.")
    return arr


def impose_dirichlet(V: np.ndarray, left, right, top, bottom) -> None:
    """
    Aplica condiciones de frontera de Dirichlet sobre la malla de potencial ``V`` in-place.

    Las fronteras se interpretan según el convenio de indexación ``V[y, x]``:

    - **left**  → ``V[:, 0]``  
    - **right** → ``V[:, -1]``  
    - **top**   → ``V[0, :]``  
    - **bottom**→ ``V[-1, :]``  

    Parameters
    ----------
    V : numpy.ndarray of shape (N, N)
        Malla del potencial sobre la cual se aplican las condiciones de frontera.
    left, right, top, bottom : float or array_like
        Valores o vectores que describen el potencial fijado en cada borde.

    Notes
    -----
    Se usa :func:`edge_to_array` internamente para asegurar que cada condición
    tenga longitud ``N``.  
    La modificación se realiza **en el mismo arreglo** para evitar copias innecesarias.
    """
    N = V.shape[0]
    from .bc import edge_to_array  # importación local para evitar dependencias circulares

    V[:, 0]  = edge_to_array(N, left)
    V[:, -1] = edge_to_array(N, right)
    V[0, :]  = edge_to_array(N, top)
    V[-1, :] = edge_to_array(N, bottom)

