def fibonacci_rec(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_rec(n-2)+fibonacci_rec(n-1)

def fibonacci_iter(n: int) -> int:
    if n == 1:
        return 1
    if n == 2:
        return 1
    
    arr = [0] * n
    arr[0] = 1
    arr[1] = 1
    for i in range(2, n):
        arr[i] = arr[i - 1] + arr[i - 2]

    return arr[n - 1]

def fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b


def main():
    n = 35
    print(f"Вычисление {n} числа Фибоначчи рекурсивно:")
    print(fibonacci_rec(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно:")
    print(fibonacci_iter(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно без использования массива:")
    print(fibonacci(n))


if __name__ == "__main__":
    main()
