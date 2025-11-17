def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно согласно
    формуле вычисления последовательности."""
    if n in (1, 2):
        return 1
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно с использованием
    массива для хранения вычисляемых данных."""
    if n in (1, 2):
        return 1
    numbers = [1] * n

    for idx in range(2, n):
        numbers[idx] = numbers[idx - 1] + numbers[idx - 2]

    return numbers[-1]


def fibonacci(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Итеративная реализация без массива."""
    fib_num1 = 1
    fib_num2 = 1

    if n in (1, 2):
        return 1
    for i in range(2, n):
        result = fib_num1 + fib_num2
        fib_num1 = fib_num2
        fib_num2 = result

    return result


def main():
    n = 35
    print(f"Вычисление {n} числа Фибоначчи рекурсивно:")
    print(fibonacci_rec(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно:")
    print(fibonacci_iter(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно без использования массива:")
    print(fibonacci_iter(n))


if __name__ == "__main__":
    main()
