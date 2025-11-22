import random
from collections import namedtuple
from main import calculate_determinant
Case = namedtuple("Case", ["matrix", "det"])
MAX_RANDOM_VALUE = 10
MIN_RANDOM_VALUE = 1

def get_det(mat):
    sum = 0
    if(len(mat) > 2):
        for i in range(len(mat)):        
            newMat = [[0 for k in range(len(mat) - 1)]for j in range(len(mat) - 1)]
            for j in range(1,len(mat)):
                count = 0
                for k in range(len(mat)):
                    if(k != i):
                        newMat[j-1][count] = mat[j][k]
                        count += 1
            sum += (-1)**(i)* mat[0][i] * get_det(newMat)
    else:
        sum += mat[1][1]*mat[0][0] - mat[0][1] * mat[1][0]
    return sum
def generate_matrix_and_det(order) -> Case:
    """Генерирует случайную квадратную целочисленную матрицу с заранее
    известным значением определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: именованный кортеж Case с полями matrix, det
    """
    matrix = []
    for i in range(order):
        matrix.append(list([int(random.random() * 100 )for i in range(order)]))
    print(matrix)
    return Case(matrix,calculate_determinant(matrix))


def main():
    n = 5
    print(f"Генерация матрицы порядка {n}")
    result = generate_matrix_and_det(n)
    print("\nОпределитель сгенерированной матрицы равен", result.det)
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in result.matrix]))


if __name__ == "__main__":
    main()
