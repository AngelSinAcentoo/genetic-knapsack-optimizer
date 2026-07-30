"""Problem model and exact reference solver."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable


@dataclass(frozen=True, order=True)
class Candidate:
    """A feasible solution and its evaluated metrics."""

    value: int
    weight: int
    genes: tuple[int, ...]


@dataclass(frozen=True)
class KnapsackProblem:
    values: tuple[int, ...]
    weights: tuple[int, ...]
    capacity: int
    max_units: int = 3

    def __post_init__(self) -> None:
        if not self.values or len(self.values) != len(self.weights):
            raise ValueError("values and weights must have the same non-zero length")
        if self.capacity <= 0 or self.max_units < 0:
            raise ValueError("capacity must be positive and max_units non-negative")
        if any(value < 0 for value in self.values):
            raise ValueError("values cannot be negative")
        if any(weight <= 0 for weight in self.weights):
            raise ValueError("weights must be positive")

    @property
    def size(self) -> int:
        return len(self.values)

    def validate_genes(self, genes: Iterable[int]) -> tuple[int, ...]:
        normalized = tuple(genes)
        if len(normalized) != self.size:
            raise ValueError(f"expected {self.size} genes")
        if any(not isinstance(gene, int) for gene in normalized):
            raise TypeError("genes must be integers")
        if any(gene < 0 or gene > self.max_units for gene in normalized):
            raise ValueError(f"genes must be between 0 and {self.max_units}")
        return normalized

    def weight(self, genes: Iterable[int]) -> int:
        normalized = self.validate_genes(genes)
        return sum(gene * weight for gene, weight in zip(normalized, self.weights))

    def value(self, genes: Iterable[int]) -> int:
        normalized = self.validate_genes(genes)
        return sum(gene * value for gene, value in zip(normalized, self.values))

    def evaluate(self, genes: Iterable[int]) -> Candidate:
        normalized = self.validate_genes(genes)
        return Candidate(
            value=self.value(normalized),
            weight=self.weight(normalized),
            genes=normalized,
        )

    def fitness(self, genes: Iterable[int], penalty: int = 10) -> int:
        candidate = self.evaluate(genes)
        excess = max(0, candidate.weight - self.capacity)
        return candidate.value - penalty * excess

    def exact_solution(self) -> Candidate:
        feasible = (
            self.evaluate(genes)
            for genes in product(range(self.max_units + 1), repeat=self.size)
            if self.weight(genes) <= self.capacity
        )
        return max(feasible)


def default_problem() -> KnapsackProblem:
    return KnapsackProblem(
        values=(4, 5, 6, 3),
        weights=(7, 6, 8, 2),
        capacity=60,
        max_units=3,
    )
