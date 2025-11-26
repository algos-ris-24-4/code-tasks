def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """

    validate_matrix_det(matrix)    
    return calculate_determinant_rec(matrix)

def calculate_determinant_rec(matrix):
    """
    Рекурсивная часть вычисления определителя
    """
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for i in range(len(matrix[0])):
        reduce = get_reduce_mat(matrix,i)
        det += matrix[0][i]*(-1)**i*calculate_determinant_rec(reduce)    
    return det


def validate_matrix(matrix):   
    """
    Проверка переменной на тип матрицы
    """
    if not type(matrix) is list:
        raise Exception("param is not matrix")
    if not type(matrix[0]) is list:
        raise Exception("param is not matrix")

def validate_matrix_det(matrix):
    """
    Проверка матрицы на возможность вычисления определителя
    """    
    validate_matrix(matrix)
    l = len(matrix)
    for i in matrix:
        if(len(i) != l):
            raise Exception("Not square matrix")
        for j in i:
            if(not type(j) in int):
                raise Exception("Not int")

def get_reduce_mat(mat, i):
    """
    Вохвращает новую матрицу с пропущенной 1 строкой и i+1 столбцом
    """
    newMat = [[0 for k in range(len(mat) - 1)]for j in range(len(mat) - 1)]
    for l in range(1,len(mat)):
        count = 0
        for k in range(len(mat)):
            if(k != i):
                newMat[l-1][count] = mat[l][k]
                count += 1
    return newMat

def main():
    matrix = [[1, 2], [3,4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
