# tests/test_solver.py
import numpy as np
from campo_estatico_mdf import LaplaceSolver2D

def test_constant_bc_converges_to_constant():
    N, c = 25, 5.0
    s = LaplaceSolver2D(N, left=c, right=c, top=c, bottom=c)
    info = s.solve_jacobi(tol=1e-6, max_iter=5000)
    assert info.max_diff < 1e-6
    # El potencial debe ser prácticamente constante en todo el dominio
    assert np.allclose(s.V, c, rtol=0.0, atol=1e-3)

    # Campo eléctrico: tolerancia adaptativa ligada a la desviación de V
    Ex, Ey = s.electric_field()
    delta_V = float(np.max(np.abs(s.V - c)))      # desviación máxima de V respecto a la constante
    thr = max(1e-6, 10.0 * delta_V)               # umbral absoluto recomendado para comparar con 0
    assert np.allclose(Ex, 0.0, rtol=0.0, atol=thr)
    assert np.allclose(Ey, 0.0, rtol=0.0, atol=thr)

def test_shapes_and_field_finite():
    s = LaplaceSolver2D(31, left=0.0, right=10.0, top=0.0, bottom=0.0)
    s.solve_jacobi(tol=1e-5, max_iter=20000)
    Ex, Ey = s.electric_field()
    assert Ex.shape == s.V.shape and Ey.shape == s.V.shape
    center_E = np.hypot(Ex[15, 15], Ey[15, 15])
    assert np.isfinite(center_E)


