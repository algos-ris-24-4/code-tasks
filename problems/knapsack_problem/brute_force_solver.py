from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

class BruteForceSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием полного перебора"""
        best_cost = 0
        best_weight = float('inf')
        best_combination = 0
        n = self.item_cnt

        #перебираем все комбинации
        total_combinations = 1
        for j in range(n):
            total_combinations *= 2

        for j in range(total_combinations):
            current_weight = 0
            current_cost = 0
            copy = j

            for i in range(n):
                bit = copy % 2
                copy = copy // 2
                if bit == 1:
                    current_weight += self.weights[i]
                    current_cost += self.costs[i]
                    if current_weight > self.weight_limit:
                        break

            if current_weight > self.weight_limit:
                continue
            if (current_cost > best_cost or
                    (current_cost == best_cost and current_weight < best_weight)):
                best_cost = current_cost
                best_weight = current_weight
                best_combination = j

        #формируем список выбранных предметов
        best_items = []
        copy = best_combination
        for i in range(n):
            bit = copy % 2
            copy = copy // 2
            if bit == 1:
                best_items.append(i)

        return KnapsackSolution(cost=best_cost, items=best_items)

if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = BruteForceSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )