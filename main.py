from collections import namedtuple
from typing import Tuple, List


class ErrorMessages:
    WRONG_COINS = (
        "Монеты должны быть представлены непустым списком положительных целых чисел"
    )
    NOT_LIST_COINS = "Монеты должны быть представлены списком"
    WRONG_AMOUNT = "Сумма размена должна быть неотрицательным целым числом"
    NOT_INT_AMOUNT = "Сумма размена должна быть целым числом"
    NOT_INT_COIN = "Монеты должны должны быть целыми числами"
    NEGATIVE_COIN = "Монеты не могут быть отрицательными или нулевыми"


CoinChangeResult = namedtuple("CoinChangeResult", ["count", "combination"])


def coin_change(coins: List[int], amount: int) -> CoinChangeResult:
    """
    Основная функция для решения задачи о размене монет.

    Args:
        coins: Список доступных монет
        amount: Сумма для размена

    Returns:
        None если решение невозможно, иначе кортеж (количество_монет, комбинация)
    """
    _validate_input(coins, amount)
    if amount == 0:
        return CoinChangeResult(0, [])
    min_coins, coin_used = _calculate_min_coins(coins, amount)

    if min_coins[amount] == float("inf"):
        return None

    combination = _restore_combination(coin_used, amount)

    return CoinChangeResult(int(min_coins[amount]), combination)


def _calculate_min_coins(
    coins: List[int], amount: int
) -> Tuple[List[float], List[int]]:
    """
    Вычисляет минимальное количество монет для каждой суммы до общей суммы размена.

    Args:
        coins: Список монет
        amount: Целевая сумма

    Returns:
        Кортеж (min_coins, coin_used), где:
        - min_coins: список минимального количества монет для каждой суммы
        - coin_used: список последних использованных монет для каждой суммы
    """
    pass


def _restore_combination(coin_used: List[int], amount: int) -> List[int]:
    """
    Восстанавливает комбинацию монет по массиву использованных монет.

    Args:
        coin_used: Список последних использованных монет для каждой суммы
        amount: Целевая сумма

    Returns:
        Список монет, составляющих решение
    """
    pass


def _validate_input(coins: List[int], amount: int) -> None:
    """
    Валидирует входные данные для задачи о размене монет.

    Args:
        coins: Список монет
        amount: Сумма для размена

    Raises:
        TypeError: Если тип данных некорректный
        ValueError: Если значения некорректные
    """
    pass


def main():
    amount = 13
    coins = [1, 2, 5]

    print("Пример решения задачи о размене монет\n")
    print(f"У нас имеется следующий набор монет: {coins}")
    print(f"Необходимо набрать сумму: {amount}")

    result = coin_change(coins, amount)

    if result:
        print(f"Необходимо: {result.count} следующих монет {result.combination}")
    else:
        print(f"Монетами: {coins} невозможно набрать сумму: {amount}")


if __name__ == "__main__":
    main()
