# Genetic Knapsack Optimizer

Solución reproducible del problema de la mochila entera acotada mediante un
algoritmo genético. Cada tipo de objeto puede aparecer entre 0 y 3 veces.

> **English summary:** A deterministic, testable genetic algorithm for a
> bounded integer knapsack problem, including an exhaustive solver used as a
> correctness baseline.

## Problema

Maximizar:

```text
Z = 4x1 + 5x2 + 6x3 + 3x4
```

Sujeto a:

```text
7x1 + 6x2 + 8x3 + 2x4 <= 60
0 <= xi <= 3
```

El repositorio mejora la práctica original de tres maneras:

- usa una semilla configurable para reproducibilidad;
- conserva élites para no perder la mejor solución;
- compara el resultado evolutivo con una búsqueda exhaustiva.

La solución exacta de referencia es `(2, 3, 3, 2)`, con valor `47` y peso
`60`.

## Ejecutar

Requiere Python 3.11 o superior y no necesita dependencias externas.

```powershell
$env:PYTHONPATH='src'
python -m knapsack.cli
```

## Pruebas

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

## Alcance

El algoritmo está diseñado como demostración educativa. Para instancias
grandes conviene incorporar reparación de restricciones, operadores
especializados y comparación con programación dinámica.
