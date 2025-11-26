def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """
    n = len(matrix)
    
    #Проверка на матрицу 1x1
    if n == 1:
        return matrix[0][0]
    
    #Проверка на матрицу 2x2
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    #Извлекаем диагонали из матрицы
    mainDiag = []  #главная диагональ
    upperDiag = []  #над главной
    bottomDiag = []  #под главной
    
    for i in range(n):
        mainDiag.append(matrix[i][i])
    
    for i in range(n-1):
        upperDiag.append(matrix[i][i+1])
    
    for i in range(1, n):
        bottomDiag.append(matrix[i][i-1])
    
    #Вычисляем определитель по рекуррентной формуле
    det1 = mainDiag[0]  #det для n=1
    det2 = mainDiag[0] * mainDiag[1] - upperDiag[0] * bottomDiag[0] #det для n=2

    #Вычисляем для матриц большего размера
    for i in range(2, n):
        detCurrent = mainDiag[i] * det2 - upperDiag[i-1] * bottomDiag[i-1] * det1
        #Обновляем значения для следующего шага
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

