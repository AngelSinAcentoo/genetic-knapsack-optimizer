"""Small, reproducible genetic algorithm for the bounded knapsack."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .problem import Candidate, KnapsackProblem

Genes = tuple[int, ...]


@dataclass(frozen=True)
class GeneticConfig:
    population_size: int = 64
    generations: int = 100
    crossover_probability: float = 0.9
    mutation_probability: float = 0.15
    tournament_size: int = 3
    elite_count: int = 2
    seed: int = 42

    def __post_init__(self) -> None:
        if self.population_size < 2:
            raise ValueError("population_size must be at least 2")
        if self.generations < 1:
            raise ValueError("generations must be positive")
        if not 0 <= self.crossover_probability <= 1:
            raise ValueError("crossover_probability must be in [0, 1]")
        if not 0 <= self.mutation_probability <= 1:
            raise ValueError("mutation_probability must be in [0, 1]")
        if not 1 <= self.elite_count < self.population_size:
            raise ValueError("elite_count must be between 1 and population_size - 1")


class GeneticAlgorithm:
    def __init__(self, problem: KnapsackProblem, config: GeneticConfig | None = None):
        self.problem = problem
        self.config = config or GeneticConfig()
        self.random = Random(self.config.seed)

    def _random_genes(self) -> Genes:
        return tuple(
            self.random.randint(0, self.problem.max_units)
            for _ in range(self.problem.size)
        )

    def _rank_key(self, genes: Genes) -> tuple[int, int, int]:
        candidate = self.problem.evaluate(genes)
        feasible = candidate.weight <= self.problem.capacity
        return (
            self.problem.fitness(genes),
            int(feasible),
            -candidate.weight,
        )

    def _select(self, population: list[Genes]) -> Genes:
        sample = self.random.choices(population, k=self.config.tournament_size)
        return max(sample, key=self._rank_key)

    def _crossover(self, left: Genes, right: Genes) -> tuple[Genes, Genes]:
        if self.problem.size < 2:
            return left, right
        if self.random.random() > self.config.crossover_probability:
            return left, right
        point = self.random.randint(1, self.problem.size - 1)
        return left[:point] + right[point:], right[:point] + left[point:]

    def _mutate(self, genes: Genes) -> Genes:
        result = list(genes)
        for index in range(len(result)):
            if self.random.random() < self.config.mutation_probability:
                result[index] = self.random.randint(0, self.problem.max_units)
        return tuple(result)

    def solve(self) -> Candidate:
        population = [self._random_genes() for _ in range(self.config.population_size)]

        for _ in range(self.config.generations):
            population.sort(key=self._rank_key, reverse=True)
            next_population = population[: self.config.elite_count]

            while len(next_population) < self.config.population_size:
                first = self._select(population)
                second = self._select(population)
                child_a, child_b = self._crossover(first, second)
                next_population.append(self._mutate(child_a))
                if len(next_population) < self.config.population_size:
                    next_population.append(self._mutate(child_b))

            population = next_population

        feasible = [
            self.problem.evaluate(genes)
            for genes in population
            if self.problem.weight(genes) <= self.problem.capacity
        ]
        if not feasible:
            raise RuntimeError("the final population did not contain a feasible solution")
        return max(feasible)
