Instalación y uso del paquete
=============================

Instalación desde TestPyPI
--------------------------

Para instalar la versión del paquete publicada en **TestPyPI**, utiliza:

.. code-block:: bash

    pip install -i https://test.pypi.org/simple/ campo-estatico-mdf-Cogua-Neira

Esto descargará tu paquete desde TestPyPI.  
Si necesitas que las dependencias se instalen desde PyPI normal, puedes usar:

.. code-block:: bash

    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple campo-estatico-mdf-Cogua-Neira


Verificar la instalación
------------------------

Para comprobar que el paquete se instaló correctamente:

.. code-block:: bash

    python -c "import campo_estatico_mdf; print('OK')"


Ejemplo de uso
--------------

Aquí tienes un ejemplo básico usando el solver 2D incluido en tu paquete:

.. code-block:: python

    from campo_estatico_mdf.solver import LaplaceSolver2D

    solver = LaplaceSolver2D(
        N=50,
        left=0.0,
        right=10.0,
        top=5.0,
        bottom=0.0,
    )

    info = solver.solve_jacobi(tol=1e-5, max_iter=10000)

    print("Iteraciones:", info.iterations)
    print("Diferencia final:", info.max_diff)


Ejemplo de visualización
------------------------

Si además quieres graficar el potencial y el campo eléctrico:

.. code-block:: python

    from campo_estatico_mdf.visual import plot_potential, plot_field
    import matplotlib.pyplot as plt

    # graficar potencial
    fig1 = plot_potential(solver.V)
    plt.show()

    # graficar campo eléctrico
    fig2 = plot_field(solver.V, solver.h, stride=2)
    plt.show()


Actualizar a la última versión
------------------------------

Para actualizar el paquete:

.. code-block:: bash

    pip install -U -i https://test.pypi.org/simple/ campo-estatico-mdf-Cogua-Neira


Ejecutar las pruebas (opcional)
-------------------------------

Si clonas el repositorio y quieres correr los tests:

.. code-block:: bash

    pytest -q
