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

        #перебираем все комбинации
        total_combinations = 2 ** self.item_cnt

        for j in range(total_combinations):

            selected_items = [False] * self.item_cnt
            copy = j
            
            for i in range(self.item_cnt):
                if (j >> i) & 1:
                    selected_items[i] = True
            
            current_weight = self.get_weight(selected_items)
            current_cost = self.get_cost(selected_items)
            

            if current_cost == 0:
                continue
                
            if (current_cost > best_cost or
                    (current_cost == best_cost and current_weight < best_weight)):
                best_cost = current_cost
                best_weight = current_weight
                best_combination = j

        #формируем список выбранных предметов
        best_items = []
        copy = best_combination
        for i in range(self.item_cnt):
            if (best_combination >> i) & 1:
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