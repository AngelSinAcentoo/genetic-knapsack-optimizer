from __future__ import annotations

import unittest

from knapsack import GeneticAlgorithm, KnapsackProblem, default_problem


class KnapsackProblemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.problem = default_problem()

    def test_exact_solution_matches_known_optimum(self) -> None:
        result = self.problem.exact_solution()
        self.assertEqual((47, 60, (2, 3, 3, 2)), (result.value, result.weight, result.genes))

    def test_penalty_reduces_infeasible_fitness(self) -> None:
        infeasible = (3, 3, 3, 3)
        self.assertEqual(54, self.problem.value(infeasible))
        self.assertEqual(69, self.problem.weight(infeasible))
        self.assertEqual(-36, self.problem.fitness(infeasible))

    def test_rejects_invalid_problem(self) -> None:
        with self.assertRaises(ValueError):
            KnapsackProblem(values=(1,), weights=(), capacity=10)

    def test_genetic_algorithm_reaches_optimum_with_default_seed(self) -> None:
        genetic = GeneticAlgorithm(self.problem).solve()
        exact = self.problem.exact_solution()
        self.assertEqual(exact.value, genetic.value)
        self.assertLessEqual(genetic.weight, self.problem.capacity)


if __name__ == "__main__":
    unittest.main()
