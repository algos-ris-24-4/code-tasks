def calculate_determinant(matrix: list[list[int]]) -> int:
    
    if matrix is None:
        raise Exception("Матрицы нет")
    if not matrix or len(matrix) == 0:
        raise Exception("Матрица не может быть пустая")
    n = len(matrix)
    
    for row in matrix:
        if len(row) != n:
            raise Exception("Матрица должна быть пропорциональной")
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col + 1:] for row in matrix[1:]]
        cofactor = ((-1) ** col) * matrix[0][col] * calculate_determinant(minor)
        det += cofactor
    return det

def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
