def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """
    n = len(matrix)
    a = matrix[0][0]
    b = matrix[0][1] if n > 1 else None
    c = matrix[1][0] if n > 1 else None

    validate(a, b, c, matrix)
    
    return calculate_determinant(a, b, c, n)

def calculate_determinant(a, b, c, size):
    if size == 1:
        return a
    if size == 2:
        return a ** 2 - b * c
    return a * calculate_determinant(a, b, c, size - 1) - b * c * calculate_determinant(a, b, c, size - 2)

def validate(a, b, c, matrix):
    """Проверяет матрицу на правильность и кидает Exception"""
    if matrix is None:
        raise Exception("Матрица не может быть None")
    if len(matrix) == 0:
        raise Exception("Матрица не заполнена")
    n = len(matrix)
    
    for i, row in enumerate(matrix):
        if row is None or len(row) != len(matrix):
            raise Exception("Матрица должна быть квадратной")
    for i in range(n):
        for j in range(n):
            if i == j:
                if matrix[i][j] != a:
                    raise Exception("Значение на главной диагонали неправильное")
            elif i == j - 1:
                if matrix[i][j] != b:
                    raise Exception("Значение на верхней диагонали неправильное")
            elif i == j + 1:
                if matrix[i][j] != c:
                    raise Exception("Значение на нижней диагонали неправильное")
            else:
                if matrix[i][j] != 0:
                    raise Exception("Не ноль вне трех диагоналей")

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()