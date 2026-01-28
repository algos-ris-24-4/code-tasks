from unittest import TestLoader, TestSuite, TextTestRunner

from tests.problems.sorting_problem.test_quick_sort import TestQuickSort


def suite():
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestQuickSort))
    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
