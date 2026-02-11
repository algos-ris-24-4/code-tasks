from unittest import TestLoader, TestSuite, TextTestRunner

from tests.problems.shortest_path_problem.test_bellman_ford import TestBellmanFord


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestBellmanFord))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
