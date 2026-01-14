from collections import namedtuple

from enum import StrEnum


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках."""

    WRONG_MATRIX = (
        "Таблица прибыли от проектов не является прямоугольной "
        "матрицей с числовыми значениями"
    )
    NEG_PROFIT = "Значение прибыли не может быть отрицательно"
    DECR_PROFIT = "Значение прибыли не может убывать с ростом инвестиций"


Result = namedtuple("Result", ["profit", "distribution"])


class ProfitValueError(Exception):
    def __init__(self, message, project_idx, row_idx):
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def validate(profit_matrix: list[list[int]]):
    """
    Валидирует таблицу с распределением прибыли от проектов, поступающую на вход.
    
    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :raise ValueError: Если таблица прибыли от проектов не является
    прямоугольной матрицей с числовыми значениями.
    :raise ProfitValueError: Если значение прибыли отрицательно или убывает
    с ростом инвестиций.
    """

    # Проверка типа и количества уровней инвестиций (строки)
    if not isinstance(profit_matrix, list) or len(profit_matrix) == 0:
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    # Проверка типа и количества проектов (столбцы)
    if not isinstance(profit_matrix[0], list) or len(profit_matrix[0]) == 0:
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    invest_lvl_cnt = len(profit_matrix)
    project_cnt = len(profit_matrix[0]) 

    # Проверка прямоугольности
    for ivest_lvl_row in profit_matrix:
        if len(ivest_lvl_row) != project_cnt:
            raise ValueError(ErrorMessages.WRONG_MATRIX)

    # Проверка значений прибыли
    for project in range(project_cnt):
        prev_profit = -1

        for invest_lvl in range(invest_lvl_cnt):
            profit = profit_matrix[invest_lvl][project]

            if not isinstance(profit, int):
                raise ValueError(ErrorMessages.WRONG_MATRIX)
            
            if profit < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project, invest_lvl)
            
            if profit < prev_profit:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, project, invest_lvl)
            else:
                prev_profit = profit


def get_invest_distribution(profit_matrix: list[list[int]]) -> Result:
    """Рассчитывает максимально возможную прибыль и распределение инвестиций
    между несколькими проектами. Инвестиции распределяются кратными частями.

    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :raise ValueError: Если таблица прибыли от проектов не является
    прямоугольной матрицей с числовыми значениями.
    :raise ProfitValueError: Если значение прибыли отрицательно или убывает
    с ростом инвестиций.
    :return: именованный кортеж Result с полями:
    profit - максимально возможная прибыль от инвестиций,
    distribution - распределение инвестиций между проектами.
    """

    validate(profit_matrix)

    




    return


def get_distribution(invest_lvl_max: int, projects_cnt: int, dp: list[list[int]]) -> list[int]:
    """Восстановление пути распределения инвестиций по проектам"""

    ...


def main():
    profit_matrix = [
        [15, 18, 16, 17],
        [20, 22, 23, 19],
        [26, 28, 27, 25],
        [34, 33, 29, 31],
        [40, 39, 41, 37],
    ]
    print(get_invest_distribution(profit_matrix))


if __name__ == "__main__":
    main()
