# src/campo_estatico_mdf/__init__.py
from .solver import LaplaceSolver2D
from .jacobi import ConvergenceInfo

__all__ = ["LaplaceSolver2D", "ConvergenceInfo"]
