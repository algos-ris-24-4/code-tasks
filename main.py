import time

from profilehooks import profile


def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно согласно
    формуле вычисления последовательности.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n == 1 or n == 2:
        return 1
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно с использованием
    массива для хранения вычисляемых данных.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n == 1 or n == 2:
        return 1

    seq = [0] * n
    seq[0] = 1
    seq[1] = 1

    for i in range(2, n):
        seq[i] = seq[i - 1] + seq[i - 2]

    return seq[n - 1]


def fibonacci(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно без использования массива.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n == 1 or n == 2:
        return 1
    prev, curr = 1, 1
    for i in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


@profile
def main():
    n = 35

    print(f"Вычисление {n}-го числа Фибоначчи рекурсивно:")
    start = time.perf_counter()
    result_rec = fibonacci_rec(n)
    elapsed_rec = (time.perf_counter() - start) * 1000
    print(f"{result_rec} (время выполнения: {elapsed_rec:.4f} мс)\n")

    print(f"Вычисление {n}-го числа Фибоначчи итеративно (с массивом):")
    start = time.perf_counter()
    result_iter = fibonacci_iter(n)
    elapsed_iter = (time.perf_counter() - start) * 1000
    print(f"{result_iter} (время выполнения: {elapsed_iter:.4f} мс)\n")

    print(f"Вычисление {n}-го числа Фибоначчи итеративно (без массива):")
    start = time.perf_counter()
    result_opt = fibonacci(n)
    elapsed_opt = (time.perf_counter() - start) * 1000
    print(f"{result_opt} (время выполнения: {elapsed_opt:.4f} мс)\n")


if __name__ == "__main__":
    main()
