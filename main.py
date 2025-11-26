def validate_matrix(matrix: list[list[int]]):
    """
    Выполняет валидацию входной матрицы на соответствие требованиям:
    - матрица не None и не пустая;
    - представлена как список списков целых чисел;
    - является квадратной;
    - является трёхдиагональной (все элементы вне главной и побочных диагоналей (|i - j| ≤ 1) равны нулю);
    - все элементы на главной диагонали одинаковы;
    - все элементы на верхней побочной диагонали (правее главной) одинаковы;
    - все элементы на нижней побочной диагонали (левее главной) одинаковы;

    Если хотя бы одно из условий не выполняется выбрасывается исключение:

    :raises TypeError: если matrix не является списком или содержит нецелые элементы
    :raises ValueError: если матрица пуста, не квадратна, не трёхдиагональна, диагонали неоднородны.
    """
    matrix_len = len(matrix)  # Ранг матрицы

    # Проверка на None
    if matrix is None:
        raise TypeError(
            "Error! Input must be a matrix represented as a list of lists of equal length"
        )

    # Проверка на список
    if type(matrix) is not list:
        raise TypeError(
            "Error! Input must be a matrix represented as a list of lists of equal length"
        )

    # Проверка, что матрица не пустая
    if matrix_len == 0:
        raise ValueError(
            "Error! Empty matrix provided. Input must be a matrix represented as a list of lists of equal length"
        )

    # Проверка размерности матрицы, что состоит из списков целых чисел и списков одинаковой длины(не ступенчатая/рваная/не прямоугольная)
    for i in range(matrix_len):
        row = matrix[i]
        if type(row) is not list:
            raise TypeError(
                f"Error! Row {i} is not a list. Input must be a matrix represented as a list of lists of equal length"
            )
        if len(row) != matrix_len:
            raise ValueError(
                f"Error! Matrix is not square, row ({i}) has length different from column length ({matrix_len}). Input must be a matrix represented as a list of lists of equal length "
            )
        # Проверка на целое число
        for j in range(matrix_len):
            elem = row[j]
            if type(elem) is not int:
                raise TypeError(
                    f"Error! Element ({elem}) in row ({i}) at position ({j}) is not an integer"
                )

    # Проверка на трёхдиагональность, все элементы не на диагоналях должны быть нулевыми
    for i in range(matrix_len):
        for j in range(matrix_len):
            if abs(i - j) > 1:
                if matrix[i][j] != 0:
                    raise ValueError(
                        f"Error! Matrix does not satisfy tridiagonal condition. Non-zero element ({matrix[i][j]}) found at position ({i}, {j})"
                    )

    # Проверка, что все элементы главной диагонали одинаковы
    if matrix_len >= 1:
        first_main = matrix[0][0]
        for i in range(1, matrix_len):
            if matrix[i][i] != first_main:
                raise ValueError("Error! Main diagonal elements are not identical")

    # Проверка, что все элементы наддиагонали одинаковы
    if matrix_len >= 2:
        first_upper = matrix[0][1]
        for i in range(0, matrix_len - 1):
            if matrix[i][i + 1] != first_upper:
                raise ValueError(
                    "Error! Upper side-diagonal elements are not identical"
                )

    # Проверка, что все элементы поддиагонали одинаковы
    if matrix_len >= 2:
        first_lower = matrix[1][0]
        for i in range(0, matrix_len - 1):
            if matrix[i + 1][i] != first_lower:
                raise ValueError(
                    "Error! Lower side-diagonal elements are not identical"
                )


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
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] ** 2 - matrix[0][1] * matrix[1][0]

    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    n = len(matrix)

    reduced_matrix_1 = get_reduced_matrix(matrix, n - 1)
    reduced_matrix_2 = get_reduced_matrix(matrix, n - 2)
    return a * get_tridiagnal_determinant_recursive(
        reduced_matrix_1
    ) - b * c * get_tridiagnal_determinant_recursive(reduced_matrix_2)


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.

    :param matrix: целочисленная трехдиагональная квадратная матрица.
    :raises TypeError: если matrix не является списком или содержит нецелые элементы
    :raises ValueError: если матрица пуста, не квадратна, не трёхдиагональна, диагонали неоднородны.
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
