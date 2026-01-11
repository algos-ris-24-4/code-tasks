from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)


class DynamicSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """
        Решает задачу о рюкзаке с использованием метода динамического программирования.

        :return: максимально возможная общая стоимость и список индексов выбранных предметов
        :rtype: KnapsackSolution
        """
        i_cnt = self.item_cnt
        w_limit = self.weight_limit
        weights = self.weights
        costs = self.costs

        table = [[0] * (w_limit+1) for _ in range(i_cnt+1)]

        for i in range(1, i_cnt + 1):
            wi = weights[i-1]
            ci = costs[i-1]
            for j in range(w_limit + 1):
                table[i][j] = table[i-1][j]
                if wi <= j:
                    cost = table[i-1][j-wi] + ci
                    if cost > table[i][j]:
                        table[i][j] = cost

        idxs = [] 
        w = w_limit

        for i in range(i_cnt, 0, -1):
            if table[i][w] != table[i-1][w]:
                idxs.append(i-1)
                w -= weights[i-1]

        idxs.reverse()

        result = table[i_cnt][w_limit]

        return KnapsackSolution(result, idxs)

        


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = DynamicSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
