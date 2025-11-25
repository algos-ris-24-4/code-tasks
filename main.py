import copy
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
       reduced_matrix = get_reduced_matrix(matrix, 0, idx)
       det += item * (-1)**idx * calculate_determinant(reduced_matrix)
    return det

def get_reduced_matrix(matrix, row_idx, col_idx):
    ans_matrix = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        ans_matrix[i] = ans_matrix[i][:col_idx] + ans_matrix[i][col_idx + 1:]
    ans_matrix = ans_matrix[:row_idx] + ans_matrix[row_idx + 1:]
    return ans_matrix


def validate(matrix):
    if not isinstance(matrix, list):
        raise Exception("Ошибка: Входные данные не являются списком.")

    if len(matrix) == 0:
        raise Exception("Ошибка: Матрица пуста.")

    for row in matrix:
        if not isinstance(row, list):
            raise Exception("Ошибка: Строки матрицы не являются списками.")
        if len(row) != len(matrix):
            raise Exception("Ошибка: Матрица не является квадратной.")

    for row in matrix:
        for element in row:
            if not isinstance(element, int):
                raise Exception("Ошибка: Матрица содержит нецелочисленные элементы.")



def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
