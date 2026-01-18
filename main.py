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


def _validate_matrix(profit_matrix: list[list[int]]) -> tuple[int, int]:
    
    if not profit_matrix or not isinstance(profit_matrix, list):
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    if not profit_matrix[0] or not isinstance(profit_matrix[0], list):
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    n_levels = len(profit_matrix)
    n_projects = len(profit_matrix[0])

    for row_idx, row in enumerate(profit_matrix):
        if not isinstance(row, list) or len(row) != n_projects:
            raise ValueError(ErrorMessages.WRONG_MATRIX)

        for project_idx, value in enumerate(row):
            if not isinstance(value, (int, float)):
                raise ValueError(ErrorMessages.WRONG_MATRIX)

            if value < 0:
                raise ProfitValueError(
                    ErrorMessages.NEG_PROFIT, project_idx, row_idx
                )

            if row_idx > 0:
                prev_value = profit_matrix[row_idx - 1][project_idx]
                if value < prev_value:
                    raise ProfitValueError(
                        ErrorMessages.DECR_PROFIT, project_idx, row_idx
                    )

    return n_levels, n_projects


def _calculate_dp_table(
    profit_matrix: list[list[int]], n_levels: int, n_projects: int
) -> list[list[int]]:
    
    dp = [[0] * (n_levels + 1) for _ in range(n_projects + 1)]

    for k in range(1, n_projects + 1):
        for m in range(n_levels + 1):
            for invest in range(m + 1):
                profit = 0
                if invest > 0:
                    profit = profit_matrix[invest - 1][k - 1]

                dp[k][m] = max(dp[k][m], dp[k - 1][m - invest] + profit)

    return dp


def _restore_distribution(
    dp: list[list[int]],
    profit_matrix: list[list[int]],
    n_levels: int,
    n_projects: int,
) -> list[int]:
    
    distribution = [0] * n_projects
    remaining = n_levels

    for k in range(n_projects, 0, -1):
        for invest in range(remaining + 1):
            profit = 0
            if invest > 0:
                profit = profit_matrix[invest - 1][k - 1]

            if dp[k][remaining] == dp[k - 1][remaining - invest] + profit:
                distribution[k - 1] = invest
                remaining -= invest
                break

    return distribution


def get_invest_distribution(
    profit_matrix: list[list[int]],
) -> Result:
    
    n_levels, n_projects = _validate_matrix(profit_matrix)
    dp = _calculate_dp_table(profit_matrix, n_levels, n_projects)
    distribution = _restore_distribution(
        dp, profit_matrix, n_levels, n_projects
    )

    return Result(profit=dp[n_projects][n_levels], distribution=distribution)


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
