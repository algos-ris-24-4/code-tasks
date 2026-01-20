import unittest

from problems.sorting_problem.merge_sort import merge_sort
from tests.problems.sorting_problem.test_abstract import TestAbstractSorter


class TestMergeSort(unittest.TestCase, TestAbstractSorter):
    """Набор тестов для проверки некоторого метода сортировки."""

    sort_method = lambda _, items: merge_sort(items)


if __name__ == "__main__":
    unittest.main()
