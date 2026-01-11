import unittest

from problems.knapsack_problem.dynamic_solver import DynamicSolver
from problems.knapsack_problem.errors.error_message_enum import ErrorMessageEnum
from tests.problems.knapsack_problem.test_abstract import TestAbstractSolver
from problems.knapsack_problem.errors.error_message_template import ErrorMessageTemplateEnum
from problems.knapsack_problem.errors.constants import WEIGHTS
class TestDynamicSolver(unittest.TestCase, TestAbstractSolver):
    """Набор тестов для проверки решения задачи о рюкзаке методом
    динамического программирования."""

    solver = DynamicSolver

    def test_float_in_weights(self):
        """Проверяет выброс исключения при передаче не целочисленного значения
        в списке весов."""
        with self.assertRaises(TypeError) as error:
            self.solver([1, 1.1], [1, 1], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_INT.format(WEIGHTS),
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
