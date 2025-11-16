#  Potencial Electroestático 2D — `campo_estatico_mdf`

Simulación numérica del **potencial eléctrico** y el **campo eléctrico** en una región 2D usando la **Ecuación de Laplace** y el **Método de Diferencias Finitas (MDF)**.  
Este proyecto incluye:

- **Backend científico** (`campo_estatico_mdf`): resolución iterativa con **Jacobi / Gauss–Seidel**.  
- **Cálculo del campo eléctrico**: `E = -∇V`.  
- **Interfaz interactiva** con **Streamlit**.  
- **Pruebas unitarias** (pytest/unittest).  
- **Documentación profesional** con **Sphinx + GitHub Pages**.

---

## Características Principales

- Resolución numérica robusta de la **Ecuación de Laplace en 2D**

  $$\nabla^2 V = 0$$

- Implementación del **Método de Diferencias Finitas**:

  $$V_{i,j} = \frac{1}{4} \left( V_{i+1,j} + V_{i-1,j} + V_{i,j+1} + V_{i,j-1} \right)$$

- Métodos iterativos disponibles:
  - Jacobi  
  - Gauss–Seidel  

- Cálculo del campo eléctrico:

  $$\vec{E} = -\nabla V$$


- Visualización:
  - Mapa de calor del potencial (heatmap)
  - Gráfico de flechas del campo eléctrico (quiver plot)
