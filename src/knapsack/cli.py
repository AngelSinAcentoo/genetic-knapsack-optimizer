"""Command-line demonstration."""

from __future__ import annotations

from .ga import GeneticAlgorithm
from .problem import default_problem


def main() -> None:
    problem = default_problem()
    genetic = GeneticAlgorithm(problem).solve()
    exact = problem.exact_solution()

    print("Genetic solution")
    print(f"  genes:  {genetic.genes}")
    print(f"  value:  {genetic.value}")
    print(f"  weight: {genetic.weight}")
    print("Exact baseline")
    print(f"  genes:  {exact.genes}")
    print(f"  value:  {exact.value}")
    print(f"  weight: {exact.weight}")
    print(f"Optimality gap: {exact.value - genetic.value}")


if __name__ == "__main__":
    main()
