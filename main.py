from collections import namedtuple


INF = float("inf")
PARAM_ERR_MSG = "Таблица цен не является прямоугольной матрицей с числовыми значениями"

Result = namedtuple("Result", ["cost", "path"])

def validate(table):
    if table is None:
        raise ValueError(PARAM_ERR_MSG)
    
    if not isinstance(table, list):
        raise ValueError(PARAM_ERR_MSG)
    
    if len(table) == 0:
        raise ValueError(PARAM_ERR_MSG)
    
    if not isinstance(table[0], list) or len(table[0]) == 0:
        raise ValueError(PARAM_ERR_MSG)
    
    col_count = len(table[0])
    for row in table:
        if not isinstance(row, list):
            raise ValueError(PARAM_ERR_MSG)
        
        if len(row) != col_count:
            raise ValueError(PARAM_ERR_MSG)
        
        for element in row:
            if not isinstance(element, int) and not isinstance(element, float):
                raise ValueError(PARAM_ERR_MSG)
    
        
    
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
    validate(price_table)
    
    row_count = len(price_table) 
    col_count = len(price_table[0])
    path_count = [[INF] * col_count for _ in range(row_count)]
    parent = [[None] * col_count for _ in range(row_count)]
    
    path_count[0][0] = price_table[0][0]
    
    for i in range(1, col_count):
        path_count[0][i] = path_count[0][i - 1] + price_table[0][i]
        parent[0][i] = (0, i - 1)
    
    for i in range(1, row_count):
        path_count[i][0] = path_count[i - 1][0] + price_table[i][0]
        parent[i][0] = (i - 1, 0)
    
    for i in range(1, row_count):
        for j in range(1, col_count):
            min_prev = min(path_count[i - 1][j], path_count[i][j - 1])
            path_count[i][j] = min_prev + price_table[i][j]
            if path_count[i - 1][j] <= path_count[i][j - 1]:
                parent[i][j] = (i - 1, j)
            else:
                parent[i][j] = (i, j - 1)
    
    path = []
    i, j = row_count - 1, col_count - 1
    while i is not None and j is not None:
        path.append((i, j))
        p = parent[i][j]
        if p is None:
            break
        i, j = p
    path.reverse()
    
    return Result(cost=path_count[row_count - 1][col_count - 1], path=path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
