import time


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """

    if len(matrix) == 0 or len(matrix[0]) == 0:
        raise Exception("Матрица не может быть пустой")

    n = len(matrix)

    for row in matrix:
        if len(row) != n:
            raise Exception("Матрица должна быть квадратной")
        for element in row:
            if type(element) is not int:
                raise Exception("Все элементы матрицы должны быть целыми числами")

    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for j in range(n):
        minor = []
        for i in range(1, n):
            minor_row = []
            for k in range(n):
                if k != j:
                    minor_row.append(matrix[i][k])
            minor.append(minor_row)

        minor_det = calculate_determinant(minor)
        determinant += (-1) ** j * matrix[0][j] * minor_det

    return determinant


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица:")
    for row in matrix:
        print(row)

    start = time.perf_counter()
    result = calculate_determinant(matrix)
    elapsed = (time.perf_counter() - start) * 1000  # в миллисекундах

    print(f"Определитель матрицы равен {result}")
    print(f"Время выполнения: {elapsed:.4f} мс")


if __name__ == "__main__":
    main()
