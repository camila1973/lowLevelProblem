# Low Level Problem — DAG (Covalto)

Solución en Python para:
- Vértice más alcanzable (DP + orden topológico)
- Caminos a V ordenados por costo (DFS)
- Inserción de V' cumpliendo (3.a) y (3.b)

## Requisitos

- Python 3.8+
- Sin dependencias externas

## Estructura

```
.
├─ low_level_problem.py
└─ tests/
   └─ tests.py
```

## Ejecutar por ítem

Desde la raíz del repo:

```bash
# Ítem 1: V más alcanzable
python low_level_problem.py 1

# Ítem 2: Caminos a V ordenados por costo
python low_level_problem.py 2

# Ítem 3: Proponer inserción de V' (valida 3.a y 3.b)
python low_level_problem.py 3

# Ítem 4: Mensaje si (3.b) es imposible
python low_level_problem.py 4

# Ítem 5: Imprime aristas {u, v, w} para insertar V' (si es posible)
python low_level_problem.py 5

# Item 6: insertar V' permitiendo V->V' (flujo exitoso)
python low_level_problem.py 6   

```

El grafo de ejemplo está en `EDGES` dentro de `low_level_problem.py`. Cambia esa constante si quieres probar otro caso.

## Correr tests

```bash
# Ejecuta el archivo de pruebas directamente
python -m unittest -v tests/tests.py
```

Si más adelante renombras a `test_*.py`, podrás usar simplemente:

```bash
python -m unittest -v
```
