def calculate_determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    det = 0
    
    if matrix is None or n == 0:
        raise Exception("Матрица не может быть None или пустой")
    
    if any(any(not isinstance(x, int) for x in row) for row in matrix):
        raise Exception("Все элементы матрицы должны быть целыми числами")
    
    for row in matrix:
        if len(row) != n:
            raise Exception("Матрица не является квадратной")
        
    if n == 1:
        return matrix[0][0]
    
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    else:
        for j in range(n):
        
            minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        
            sign = 1 if j % 2 == 0 else -1
        
            det += sign * matrix[0][j] * calculate_determinant(minor)

    return det



def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
