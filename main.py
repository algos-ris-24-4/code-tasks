def validate_matrix(matrix: list[list[int]]):
    pass


def get_reduced_matrix(matrix: list[list[int]], order: int) -> list[list[int]]:
    """
    Генерирует матрицу порядка n - 1 с помощью глубокого копирования исходной матрицы
    
    :param matrix: исходная матрица
    :type matrix: list[list[int]]
    :param order: порядок генерируемой матрицы
    :type order: int
    :return: Матрица порядка order
    :rtype: list[list[int]]
    """
    new_matrix = [[0] * order for _ in range(order)]
    for row_idx in range(order):
        for col_idx in range(order):
            new_matrix[row_idx][col_idx] = matrix[row_idx + 1][col_idx + 1]
    return new_matrix


def get_tridiagnal_determinant_recursive(matrix: list[list[int]]) -> int:
    """Рекурсивно вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """
    if len(matrix) == 1: return matrix[0][0]
    if len(matrix) == 2: return matrix[0][0] ** 2 - matrix[0][1] * matrix[1][0]

    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    n = len(matrix)

    reduced_matrix_1 = get_reduced_matrix(matrix, n - 1)
    reduced_matrix_2 = get_reduced_matrix(matrix, n - 2)
    return a * get_tridiagnal_determinant_recursive(reduced_matrix_1) - b * c * get_tridiagnal_determinant_recursive(reduced_matrix_2)


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.
    :raise Exception: ...
    :return: значение определителя.
    """
    validate_matrix(matrix)
    return get_tridiagnal_determinant_recursive(matrix)


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
