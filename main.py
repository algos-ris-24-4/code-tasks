def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    validate(matrix)

    if len(matrix) == 1:
        return matrix[0][0]

    det = 0
    for idx, item in enumerate(matrix[0]):
        reduced_matrix = get_reduced_matrix(matrix, idx)
        det += item * (-1)**idx * calculate_determinant(reduced_matrix)
    return det

def get_reduced_matrix(matrix, column):
    result = []
    for i in range(1, len(matrix)):
        current_row = matrix[i]
        result.append(current_row[:column] + current_row[column + 1:])
    return result

def validate(matrix: list[list[int]]):
    if not matrix or not isinstance(matrix,list):
        raise Exception("Матрица должна быть непустым списком")
    length = len(matrix)
    for i in range(len(matrix)):
        row = matrix[i]
        if not isinstance(row,list):
            raise Exception("Каждый ряд матрицы должен быть списком чисел")
        if len(row) != len(matrix):
            raise Exception("Матрица должна быть квадратной")
        for j in row:
            if not isinstance(j,int):
                raise Exception("Каждый элемент матрицы должен быть целым числом")


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
