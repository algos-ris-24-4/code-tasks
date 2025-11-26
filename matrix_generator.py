import random
from collections import namedtuple

Case = namedtuple("Case", ["matrix", "det"])
MAX_RANDOM_VALUE = 10
MIN_RANDOM_VALUE = 1

def determinant(n):
    size = len(n)
    if size == 1:
        return n[0][0]
    if size == 2:
        return n[0][0] * n[1][1] - n[0][1] * n[1][0]
    total = 0
    for col in range(size):
        minor = [row[:col] + row[col + 1:] for row in n[1:]]
        total+=((-1)**col) * n[0][col]*determinant(minor)
    return total


def generate_matrix_and_det(order) -> Case:
    """Генерирует случайную квадратную целочисленную матрицу с заранее
    известным значением определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: именованный кортеж Case с полями matrix, det
    """
    if not isinstance(order, int) or order <1:
        raise ValueError("Ошибка.")
    matrix = [
        [random.randint(MIN_RANDOM_VALUE, MAX_RANDOM_VALUE) for i in range(order)]
        for i in range(order)
    ]
    det = determinant(matrix)
    return Case(matrix, det)
        
def main():
    n = 10
    print(f"Генерация матрицы порядка {n}")
    result = generate_matrix_and_det(n)
    print("\nОпределитель сгенерированной матрицы равен", result.det)
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in result.matrix]))


if __name__ == "__main__":
    main()
