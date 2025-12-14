import unittest

from main import coin_change, ErrorMessages


class TestCoinChange(unittest.TestCase):

    def __check_solution(self, coins: list[int], amount: int, result):
        """Проверяет корректность решения"""

        self.assertEqual(result.count, len(result.combination))
        self.assertEqual(sum(result.combination), amount)
        self.assertTrue(all(coin in coins for coin in result.combination))

    def test_none_coins(self):
        """Проверяет выброс исключения при передаче None в качестве coins"""
        self.assertRaisesRegex(
            TypeError, ErrorMessages.NOT_LIST_COINS, coin_change, None, 10
        )

    def test_empty_coins(self):
        """Проверяет выброс исключения при передаче пустого списка coins"""
        self.assertRaisesRegex(
            ValueError, ErrorMessages.WRONG_COINS, coin_change, [], 10
        )

    def test_none_amount(self):
        """Проверяет выброс исключения при передаче None в качестве amount"""
        self.assertRaisesRegex(
            TypeError, ErrorMessages.NOT_INT_AMOUNT, coin_change, [1, 2, 5], None
        )

    def test_negative_amount(self):
        """Проверяет выброс исключения при передаче отрицательного amount"""
        self.assertRaisesRegex(
            ValueError, ErrorMessages.WRONG_AMOUNT, coin_change, [1, 2, 5], -5
        )

    def test_negative_coin(self):
        """Проверяет выброс исключения при наличии отрицательных монет"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, -2, 5], 10)
        self.assertEqual(ErrorMessages.NEGATIVE_COIN, str(error.exception))

    def test_zero_coin(self):
        """Проверяет выброс исключения при наличии нулевых монет"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, 0, 5], 10)
        self.assertEqual(ErrorMessages.NEGATIVE_COIN, str(error.exception))

    def test_non_integer_coins(self):
        """Проверяет выброс исключения при наличии нецелочисленных монет"""
        self.assertRaisesRegex(
            TypeError,
            ErrorMessages.NOT_INT_COIN,
            coin_change,
            [1, 2.5, 5],
            10,
        )

    def test_impossible_amount(self):
        """Проверяет возврат None при невозможности набрать сумму"""
        result = coin_change([3, 7], 5)
        self.assertIsNone(result)

    def test_zero_amount(self):
        """Проверяет распределение для суммы 0"""
        coins = [1, 2, 5]
        result = coin_change(coins, 0)
        self.assertIsNotNone(result)
        self.assertEqual(result.count, 0)
        self.assertEqual(result.combination, [])
        self.__check_solution(coins, 0, result)

    def test_single_coin_solution(self):
        """Проверяет решение одной монетой"""
        coins = [1, 3, 7, 10]
        amount = 7
        result = coin_change(coins, amount)
        self.assertIsNotNone(result)
        self.assertEqual(result.count, 1)
        self.assertEqual(result.combination, [7])
        self.__check_solution(coins, amount, result)

    def test_basic_case(self):
        """Проверяет базовый случай из примера"""
        coins = [1, 2, 5]
        amount = 13
        result = coin_change(coins, amount)
        self.assertEqual(result.count, 4)
        self.assertIsNotNone(result)
        self.__check_solution(coins, amount, result)

    def test_multiple_optimal_solutions(self):
        """Проверяет случай с несколькими оптимальными решениями"""
        coins = [1, 3, 4]
        amount = 6
        result = coin_change(coins, amount)
        self.assertIsNotNone(result)
        self.assertEqual(result.count, 2)
        self.__check_solution(coins, amount, result)

    def test_us_coins(self):
        """Проверяет распределение для стандартных американских монет"""
        coins = [1, 5, 10, 25]
        amount = 99
        result = coin_change(coins, amount)
        self.assertIsNotNone(result)
        self.assertEqual(result.count, 9)
        self.__check_solution(coins, amount, result)

    def test_large_coins(self):
        """Проверяет распределение с большими монетами"""
        coins = [10, 25, 50, 100]
        amount = 155
        result = coin_change(coins, amount)
        self.assertEqual(result.count, 5)
        self.assertIsNotNone(result)
        self.__check_solution(coins, amount, result)

    def test_duplicate_coins(self):
        """Проверяет обработку дубликатов в списке монет"""
        coins = [1, 1, 2, 2, 5, 5]
        amount = 11
        result = coin_change(coins, amount)
        self.assertIsNotNone(result)
        self.assertEqual(result.count, 3)
        self.__check_solution(coins, amount, result)

    def test_single_coin_type(self):
        """Проверяет распределение для одного типа монет"""
        coins = [2]
        amount = 8
        result = coin_change(coins, amount)
        self.assertIsNotNone(result)
        self.assertEqual(result.count, 4)
        self.assertEqual(result.combination, [2, 2, 2, 2])
        self.__check_solution(coins, amount, result)

    def test_minimum_coins(self):
        """Проверяет минимальное количество монет"""
        coins = [1, 5, 10, 20, 50]
        amount = 65
        result = coin_change(coins, amount)
        self.assertIsNotNone(result)
        self.assertEqual(result.count, 3)
        self.__check_solution(coins, amount, result)


if __name__ == "__main__":
    unittest.main()
