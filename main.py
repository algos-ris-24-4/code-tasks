def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """
    n = len(matrix)
    
    """Проверка на матрицу 1x1"""
    if n == 1:
        return matrix[0][0]
    
    """Проверка на матрицу 2x2"""
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    """Вычисляем определитель по рекуррентной формуле"""
    det1 = a  #"""det для n=1"""
    det2 =a * a - b * c# """det для n=2"""

    """Вычисляем для матриц большего размера"""
    for i in range(2, n):
        detCurrent = a * det2 - b * c * det1
        #"""Обновляем значения для следующего шага"""
        det1 = det2
        det2 = detCurrent
    
    return det2


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
