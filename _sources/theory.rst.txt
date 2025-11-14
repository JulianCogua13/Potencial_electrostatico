Teoría: Diferencias Finitas y Jacobi
====================================

Ecuación de Laplace 2D
----------------------

La ecuación de Laplace en dos dimensiones describe el potencial eléctrico
en una región sin cargas:

.. math::

    \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} = 0

donde :math:`V(x,y)` es el potencial eléctrico en la posición `(x, y)`.

Esta ecuación es válida en **regiones del espacio donde la densidad de carga es cero**,
y es la base para problemas de **electrostática estacionaria**.

---

Aproximación por Diferencias Finitas
------------------------------------

Para resolver la ecuación de Laplace numéricamente, se discretiza la región
en una **malla cuadrada de N×N puntos** con paso uniforme :math:`h = \Delta x = \Delta y`.

El operador Laplaciano se aproxima usando el **esquema de cinco puntos (5-point stencil)**:

.. math::

    V_{i+1,j} + V_{i-1,j} + V_{i,j+1} + V_{i,j-1} - 4 V_{i,j} = 0

donde :math:`V_{i,j}` representa el potencial en el nodo `(i,j)` de la malla.  
Esta expresión se aplica **a todos los nodos interiores**, mientras que los nodos
en los bordes se fijan según las **condiciones de contorno Dirichlet**.

---

Método Iterativo Jacobi
-----------------------

Para resolver el sistema de ecuaciones generado por la discretización, se
utiliza un método iterativo:

1. Inicializar la matriz de potencial :math:`V` con ceros o un valor estimado.
2. Aplicar las **condiciones de contorno** en los bordes (voltajes conocidos).
3. Actualizar cada nodo interior según el promedio de sus vecinos:

   .. math::
      V_{i,j}^{new} = 0.25 * (V_{i+1,j} + V_{i-1,j} + V_{i,j+1} + V_{i,j-1})

4. Repetir hasta que la diferencia máxima entre iteraciones consecutivas
   sea menor que una tolerancia :math:`\epsilon`:

   .. math::
      \max |V_{i,j}^{new} - V_{i,j}^{old}| < \epsilon

5. Una vez convergida, se puede calcular el **campo eléctrico** usando
   el gradiente:

   .. math::
      \mathbf{E} = - \nabla V

---

Ventajas y Consideraciones
--------------------------

- El método de Jacobi es **simple y fácil de implementar**.  
- Convergencia asegurada para **sistemas diagonales dominantes**, como la discretización del Laplaciano.  
- Para mallas grandes, otros métodos iterativos como **Gauss-Seidel** o **SOR**
  pueden ser más rápidos.

---

Referencias / Bibliografía
--------------------------

1. J. D. Jackson, *Classical Electrodynamics*, 3rd Edition, Wiley, 1998.  
2. W. H. Press et al., *Numerical Recipes: The Art of Scientific Computing*, 3rd Edition, Cambridge University Press, 2007.  
3. R. L. Burden, J. D. Faires, *Numerical Analysis*, 10th Edition, Cengage Learning, 2015.  
4. M. Braun, *Differential Equations and Their Applications*, Springer, 1993.  
5. Documentación de Sphinx y reStructuredText: https://www.sphinx-doc.org/

