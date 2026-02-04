import random


def reduce_matrix(cost):
    n = len(cost)

    matrix = [row[:] for row in cost]

    for i in range(n):
        row_min = min(matrix[i])
        for j in range(n):
            matrix[i][j] -= row_min
    
    for j in range(n):
        col_min = min(matrix[i][j] for i in range(n))
        for i in range(n):
            matrix[i][j] -= col_min
    
    return matrix


def perfect_zero(matrix):
 
    n = len(matrix)

    add_arr = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                add_arr[i].append(j)
    

    matchR = [-1] * n
    visited = [False] * n
    
    def dfs(u):
        for v in add_arr[u]:
            if not visited[v]:
                visited[v] = True
                if matchR[v] == -1 or dfs(matchR[v]):
                    matchR[v] = u
                    return True
        return False
    
    matching = 0
    for u in range(n):
        visited = [False] * n
        if dfs(u):
            matching += 1
            if matching == n:
                return True
    
    return matching == n


def generate_assignment_matrix( n: int, min_cost: int = 1, max_cost: int = 100, max_attempts: int = 2000) -> list[list[int]]:
    if n < 1:
        raise ValueError("Введите число для размера матрицы")
    
    if n <= 2:
        return [[random.randint(min_cost, max_cost) for _ in range(n)] for _ in range(n)]

    range_size = max_cost - min_cost
    low_max = min_cost + max(5, range_size // 5)
    high_min = max(low_max + max(15, range_size // 3), min_cost + range_size * 2 // 3)

    if low_max >= high_min:
        high_min = max_cost
        if low_max >= high_min:
            raise ValueError("Слишком узкий диапазон для стоимости работ в матрице. Нужно увеличить max_cost")

    for _ in range(max_attempts):
        matrix = [
            [random.randint(high_min, max_cost) for _ in range(n)]
            for _ in range(n)
        ]

        for i in range(n):
            for j in range(n - 1):
                matrix[i][j] = random.randint(min_cost, low_max)

        for i in range(n):
            matrix[i][n - 1] = random.randint(high_min, max_cost)

        reduced = reduce_matrix(matrix)
        if not perfect_zero(reduced):
            return matrix

    raise ValueError(
        f"Матрицу не сгенерировалась за {max_attempts} попыток.\n"
        f"n={n}, min_cost={min_cost}, max_cost={max_cost}\n"
    )

    
if __name__ == "__main__":
    n = int(input())
    try:
        matrix = generate_assignment_matrix(n, min_cost=1, max_cost=200)
        
        print(f"Матрица {n}×{n}:")
        for row in matrix:
            print(" ".join(f"{x:4d}" for x in row))
        
        reduced = reduce_matrix(matrix)
        if perfect_zero(reduced):
            print("Найдено совершенное паросочетание после редукции. Попробуйте ещё раз")
        else:
            print("Совершенного паросочетания по нулям после редукции нет")
            
    except ValueError as e:
        print("Ошибка:", e)