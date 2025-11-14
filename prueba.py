from campo_estatico_mdf.solver import LaplaceSolver2D

solver = LaplaceSolver2D(N=10, left=0, right=10, top=0, bottom=0)
info = solver.solve_jacobi()
print(info)
