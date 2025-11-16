from campo_estatico_mdf.visual import plot_potential, plot_field
import matplotlib.pyplot as plt

fig1 = plot_potential(solver.V, figsize=(5,5))
plt.show()

fig2 = plot_field(solver.V, solver.h, stride=2, figsize=(5,5))
plt.show()
