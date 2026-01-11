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

    projects_cnt = len(profit_matrix[0])
    invest_lvl_max = len(profit_matrix)

    # Создаем матрицу для результатов дп: кортеж (максимальная прибыль, сумма инвестиций в проект)
    # Кол-во строк +1 тк добавлена строка с распределением нулевого кол-ва денег
    # Кол-во столбцов = размерности строки profit_matrix (-1 стобец - объединение проектов, +1 нулевая сумма для проекта)
    dp = [[(0, 0)] * projects_cnt for _ in range(0, invest_lvl_max + 1)]

    # Заполним заранее столбец для проекта А
    for invest_sum in range(1, len(profit_matrix) + 1):    
        dp[invest_sum][0] = profit_matrix[invest_sum - 1][0], invest_sum

    # Внешний цикл по проектам (с 1 тк проект А уже заполнен)
    for project_num in range(1, projects_cnt):     

        # Цикл по распределяемым суммам
        for curr_budget in range(0, invest_lvl_max):  

            # Хранилище для выбора максимального распределения для конкретной суммы (20: 10A+10B or 20A or 20B). 
            # Хранит  и количесво денег вложенных в проект
            dp_calc_table = [(0, 0)] 
        
            # Рассчет всех распределений для конкретной суммы между двумя проектами (+2 тк идет сдвиг из-за добавлении строки - суммы ноль, а в изначальной таблице table[0] = 10, поэтому везде будет +1)
            for curr_invest in range(0, curr_budget + 2):
                curr_profit = dp[curr_budget - curr_invest + 1][project_num - 1][0]
                if curr_invest == 0: 
                    # вся сумма вкладывается в последний подсчитанный
                    dp_calc_table.append((curr_profit, 0))
                else:  
                    # Перебор всех вариантов для суммы (хранится в виде (сумма, кол-во частей отданных в проект))
                    dp_calc_table.append((profit_matrix[curr_invest - 1][project_num] + curr_profit, curr_invest))

            # из всех сумм конкретного размера, выбираем самую выгодную
            dp[curr_budget + 1][project_num] = max(dp_calc_table, key=lambda pair: pair[0])

    distr_steps = get_distribution(invest_lvl_max, projects_cnt, dp)
    return Result(profit=dp[-1][-1][0], distribution=distr_steps)


def get_distribution(invest_lvl_max: int, projects_cnt: int, dp: list[list[int]]) -> list[int]:
    """Восстановление пути распределения инвестиций по проектам"""
    invest_sum = invest_lvl_max
    steps = [0] * projects_cnt

    for project_num in range(projects_cnt - 1, -1, -1):
        invested = dp[invest_sum][project_num][1]
        steps[project_num] = invested
        invest_sum -= invested

    return steps


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
