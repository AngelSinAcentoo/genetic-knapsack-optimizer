# Genetic Knapsack Optimizer

A reproducible genetic algorithm for a bounded integer knapsack problem. Each item type can appear from zero to three times.

## Problem

Maximize:

```text
Z = 4x1 + 5x2 + 6x3 + 3x4
```

Subject to:

```text
7x1 + 6x2 + 8x3 + 2x4 <= 60
0 <= xi <= 3
```

The portfolio version improves the original exercise in three ways:

- A configurable random seed makes runs reproducible.
- Elitism prevents the best solution from being lost between generations.
- An exhaustive solver provides a correctness baseline.

The exact reference solution is `(2, 3, 3, 2)`, with value `47` and weight `60`.

## Run

The project requires Python 3.11 or newer and has no external dependencies.

```powershell
$env:PYTHONPATH='src'
python -m knapsack.cli
```

## Tests

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

## Scope

This is an educational implementation. Larger instances would benefit from constraint-repair operators, specialized crossover and mutation strategies, and comparison with dynamic programming.
