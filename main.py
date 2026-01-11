from collections import namedtuple


INF = float("inf")
PARAM_ERR_MSG = "Таблица цен не является прямоугольной матрицей с числовыми значениями"

Result = namedtuple("Result", ["cost", "path"])


def get_min_cost_path(
    price_table: list[list[float | int]],
) -> Result:
    """Возвращает путь минимальной стоимости в таблице из левого верхнего угла
    в правый нижний. Каждая ячейка в таблице имеет цену посещения. Перемещение
    из ячейки в ячейку можно производить только по горизонтали вправо или по
    вертикали вниз.
    :param price_table: Таблица с ценой посещения для каждой ячейки.
    :raise ValueError: Если таблица цен не является прямоугольной матрицей с
    числовыми значениями.
    :return: Именованный кортеж Result с полями:
    cost - стоимость минимального пути,
    path - путь, список кортежей с индексами ячеек.
    """
    if not isinstance(price_table, list) or len(price_table) == 0:
        raise ValueError(PARAM_ERR_MSG)
    
    if not isinstance(price_table[0], list) or len(price_table[0]) == 0:
        raise ValueError(PARAM_ERR_MSG)
    
    n_cols = len(price_table[0])
    
    for row in price_table:
        if not isinstance(row, list) or len(row) != n_cols:
            raise ValueError(PARAM_ERR_MSG)
        for cell in row:
            if not (isinstance(cell, (int, float)) or cell is None):
                raise ValueError(PARAM_ERR_MSG)

    rows = len(price_table)
    cols = len(price_table[0])

    if price_table[0][0] is None or price_table[rows - 1][cols - 1] is None:
        return Result(cost=None, path=None)

    cost = [[INF] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]
    cost[0][0] = float(price_table[0][0])

    for i in range(1, rows):
        if price_table[i][0] is not None and cost[i - 1][0] != INF:
            cost[i][0] = cost[i - 1][0] + float(price_table[i][0])
            parent[i][0] = (i - 1, 0)

    for j in range(1, cols):
        if price_table[0][j] is not None and cost[0][j - 1] != INF:
            cost[0][j] = cost[0][j - 1] + float(price_table[0][j])
            parent[0][j] = (0, j - 1)

    for i in range(1, rows):
        for j in range(1, cols):
            if price_table[i][j] is None:
                continue

            from_top = cost[i - 1][j]
            from_left = cost[i][j - 1]

            if from_top <= from_left:
                if from_top != INF:
                    cost[i][j] = from_top + float(price_table[i][j])
                    parent[i][j] = (i - 1, j)
            else:
                if from_left != INF:
                    cost[i][j] = from_left + float(price_table[i][j])
                    parent[i][j] = (i, j - 1)

    if cost[rows - 1][cols - 1] == INF:
        return Result(cost=None, path=None)

    path = []
    i, j = rows - 1, cols - 1

    while (i, j) != (0, 0):
        path.append((i, j))
        i, j = parent[i][j]
        
    path.append((0, 0))
    path.reverse()

    return Result(cost=cost[rows - 1][cols - 1], path=path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    result = get_min_cost_path(table)
    
    if result.cost is None:
        print("Путь не существует")
    else:
        print(f"Минимальная стоимость: {result.cost}")
        print("Предложенный путь:")
        for step, (row, col) in enumerate(result.path, start=1):
            print(f"  Шаг {step}: ({row}, {col})")


if __name__ == "__main__":
    main()