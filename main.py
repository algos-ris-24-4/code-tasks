import time


def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    a = abs(a)
    b = abs(b)
    if(min(a,b) == 0): return max(a,b)
    count = 0
    while (a % 2 == 0 and b % 2 == 0): 
        a //= 2
        b //= 2
        count += 1
    return gcd_recursive(max(a,b) % min(a,b),min(a,b))* 2 ** count


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    a = abs(a)
    b = abs(b)
    while(min(a,b) != 0):
        if(a > b):
            a -= b
        else:
            b -= a   
    return max(a,b)


def gcd_iterative_fast(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Быстрая итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    a = abs(a)
    b = abs(b)
    count = 0
    while (a % 2 == 0 and b % 2 == 0): 
        a //= 2
        b //= 2
        count += 1
    while(min(a,b) != 0): 
        if(a > b):
            a %= b
        else:
            b %= a   
    return max(a,b) * 2 ** count


def lcm(a: int, b: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел

    :param a: натуральное число a
    :param b: натуральное число b
    :return: значение наименьшего общего кратного
    """
    return a * b / gcd_iterative_fast(a,b)

    


def main():
    a = 14
    b = 2
    print(f"Вычисление НОД чисел {a} и {b} рекурсивно:")
    start_time = time.time()
    print(gcd_recursive(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с вычитанием:")
    start_time = time.time()
    print(gcd_iterative_slow(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с делением:")
    start_time = time.time()
    print(gcd_iterative_fast(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОК чисел {a} и {b}:")
    start_time = time.time()
    print(lcm(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")


if __name__ == "__main__":
    main()
