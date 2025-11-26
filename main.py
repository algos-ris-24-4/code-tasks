def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно согласно
    формуле вычисления последовательности.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n <= 1:
        return n
    else:
        return fibonacci_rec(n-1) + fibonacci_rec(n-2)
    pass


def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно с использованием
    массива для хранения вычисляемых данных.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    fib = [0]*(n+1)
    fib[0] = 0
    if n >=1:
        fib[1] = 1
    for i in range(2, n+1):
        fib[i] = fib[i-1] + fib[i-2]

    return fib[n]
    pass


def fibonacci(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно без использования массива.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    first, second = 0, 1
    for i in range (2, n+1):
        first, second = second, first+second
    return second
    pass


def main():
    n = 35
    print(f"Вычисление {n} числа Фибоначчи рекурсивно:")
    print(fibonacci_rec(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно:")
    print(fibonacci_iter(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно без использования массива:")
    print(fibonacci_iter(n))


if name == "main":
    main()