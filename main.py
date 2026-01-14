STR_LENGTH_ERROR_MSG = "Длина строки должна быть целым положительным числом"

NOT_INT_VALUE_TEMPL = "Параметр {0} Не является целым числом"

NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"

N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def generate_strings(length: int) -> list[str]:
        
        if not isinstance(length,int) or length <= 0:
            raise ValueError(STR_LENGTH_ERROR_MSG)
        def zero(length):
            if length == 1:
                return ["0"]
            return ["0" + stroka for stroka in one(length-1)]
        
        def one(length):
            if length == 1:
                return ["1"]
            return ["1" + stroka for stroka in zero(length-1) + one(length-1)]
        
        return zero(length) + one(length)


def binomial_coefficient(n: int, k: int, use_rec=False) -> int:
    
    if not isinstance(n,int):
        raise ValueError(NOT_INT_VALUE_TEMPL.format("n"))
    if not isinstance(k,int):
        raise ValueError(NOT_INT_VALUE_TEMPL.format("k"))
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)
    
    if use_rec:
        return binomial_rec(n, k)
    else:
        return binomial_iter(n, k)
def binomial_rec(n, k):
    if k == n or k == 0:
        return 1
    return binomial_rec(n - 1, k) + binomial_rec(n - 1, k - 1)
def binomial_iter(n, k):
    if k == n or k == 0:
        return 1
    dp = [[0] * (k+1) for i in range(n+1)]
    for i in range(n + 1):
        dp[i][0] = 1
        for j in range(1, min(i, k) + 1):
            if j == i:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i-1][j] + dp[i-1][j-1]
    return dp[n][k]

def main():
    n = 2
    print(f"Строки длиной {n}:\n{generate_strings(n)}")

    n = 30
    k = 20
    print(
        f"Биномиальный коэффициент (итеративно) при n, k ({n}, {k}) = ",
        binomial_coefficient(n, k),
    )
    print(
        f"Биномиальный коэффициент (рекурсивно) при n, k ({n}, {k}) = ",
        binomial_coefficient(n, k, use_rec=True),
    )


if __name__ == "__main__":
    main()