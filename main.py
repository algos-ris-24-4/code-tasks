from collections import namedtuple

from strenum import StrEnum


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


def get_invest_distribution(
    profit_matrix: list[list[int]],
) -> Result:
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

    dp = []  # Создаем матрицу для результатов дп
    length_row = len(profit_matrix[0])
    length_column = len(profit_matrix)
    for _ in range(
        0, length_column + 1
    ):  # Кол-во строк +1 тк добавлена строка с распределением нулевого кол-ва денег
        row = [(0, 0)] * (
            length_row
        )  # Кол-во столбцов = размерности строки profit_matrix (-1 стобец - объединение проектов, +1 нулевая сумма для проекта)
        dp.append(row)

    for sum in range(
        1, len(profit_matrix) + 1
    ):  # Заполним изначально столбец для проекта А
        dp[sum][0] = profit_matrix[sum - 1][0], sum

    for number_project in range(
        1, length_row
    ):  # Внешний цикл по проектам (с 1 тк проект А уже заполнен)
        for step_sum in range(0, length_column):  # Цикл по распределяемым суммам

            dp_result = [
                (0, 0)
            ]  # Хранилище для выбора максимального распределения для конкретной суммы (20: 10A+10B or 20A or 20B). Хранит сумму и количесво денег вложенных в проект
            for x in range(
                0, step_sum + 2
            ):  # расчет всех распределений для конкретной суммы между двумя проектами (+2 тк идет сдвиг из-за добавлении строки - суммы ноль, а в изначальной таблице table[0] = 10, поэтому везде будет +1)
                if (
                    x == 0
                ):  # Если сумма вкладываемая в этот проект = 0, то вся сумма вкладывается в предподсчитанный
                    dp_result.append((dp[step_sum - x + 1][number_project - 1][0], 0))
                else:  # Перебор всех вариантов для суммы (хранится в виде (сумма,кол-во частей отданных в проект))
                    dp_result.append(
                        (
                            (
                                profit_matrix[x - 1][number_project]
                                + dp[step_sum - x + 1][number_project - 1][0]
                            ),
                            x,
                        )
                    )
            dp[step_sum + 1][number_project] = max(
                dp_result, key=lambda x: x[0]
            )  # из всех сумм конкретного размера, выбираем самую выгодную

    # Восстановление шагов инвестиций
    # Начиная из финального знач. двигаемя к нулевому (начальному) путем вычитания израсходованных частей денег
    sum_money = length_column
    steps = [0] * length_row
    for number_project in range(length_row - 1, -1, -1):
        number_invest = dp[sum_money][number_project][1]
        steps[number_project] = number_invest
        sum_money -= number_invest

    return (dp[-1][-1][0], steps)


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
