from collections import namedtuple

#from strenum import StrEnum


class ErrorMessages():
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



def validate_invest_matrix(matrix):
    """
    Проверка матрицы на возможность вычисления инвестиций
    """        
    if not type(matrix) is list:
        raise ValueError(ErrorMessages.WRONG_MATRIX)
    width = len(matrix)
    if(width == 0):
        raise ValueError(ErrorMessages.WRONG_MATRIX)
    height = len(matrix[0])    
    if not type(matrix[0]) is list:
        raise ValueError(ErrorMessages.WRONG_MATRIX) 
    if(height == 0): 
        raise ValueError(ErrorMessages.WRONG_MATRIX)
    for j in range(len(matrix[0])): 
        l = 0
        for i in range(len(matrix)):
            if(len(matrix[i]) != height):
                raise ValueError(ErrorMessages.WRONG_MATRIX)
            if(not type(matrix[i][j]) is int):
                raise ValueError(ErrorMessages.WRONG_MATRIX)
            if(matrix[i][j] < 0):
                raise ProfitValueError(ErrorMessages.NEG_PROFIT,j,i)
            
            if(l > matrix[i][j]):
                raise ProfitValueError(ErrorMessages.DECR_PROFIT,j,i)
            l = matrix[i][j]

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

    # проверяем, что матрица прямоугольная и содержит только целые неотрицательные числа
    validate_invest_matrix(profit_matrix)
    m = len(profit_matrix[0]) 
    n = len(profit_matrix)
   
    dp = [[0] * m for _ in range(n + 1)]
    
    # первый проект
    for i in range(1, n + 1):
        dp[i][0] = profit_matrix[i-1][0]
    
    # поиск максимального профита
    for j in range(1, m):
        for total in range(1, n + 1): 
            max_profit = 0
            # сколько инвестиций текущему проекту
            for k in range(total + 1):
                current_profit = profit_matrix[k-1][j] if k > 0 else 0
                remaining_profit = dp[total - k][j-1]
                max_profit = max(max_profit, current_profit + remaining_profit)
            dp[total][j] = max_profit
    


    # восстановление распределения
    distribution = [0] * m
    remaining_investment = n 
    
    # идем от последнего проекта к первому
    for j in range(m - 1, -1, -1):
        if j == 0:
            # для первого проекта все оставшиеся инвестиции
            distribution[0] = remaining_investment
            break
            
        # сколько инвестиций было дано проекту j
        for k in range(remaining_investment + 1):
            current_profit = profit_matrix[k-1][j] if k > 0 else 0
            
            # дает ли это k нужную прибыль
            if dp[remaining_investment][j] == current_profit + dp[remaining_investment - k][j-1]:
                distribution[j] = k
                remaining_investment -= k
                break
    
    max_profit = dp[n][m-1]
    
    return Result(profit=max_profit, distribution=distribution)


def main():
    profit_matrix = [
        [15, 18, 16, 17],
        [20, 22, 23, 19],
        [26, 28, 27, 25],
        [34, 33, 29, 31],
        [40, 39, 41, 37],
    ]
    data = [
    [3, 5, 4, 7, 8],
    [8, 11, 9, 8, 12],
    [9, 12, 14, 10, 13],
    [14, 16, 15, 14, 14],
    [21, 19, 20, 22, 19]
]
    newdata = [[1, -1]]
    print(get_invest_distribution(data))


if __name__ == "__main__":
    main()
