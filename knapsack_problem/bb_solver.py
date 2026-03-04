import heapq
from collections import namedtuple

from knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

KnapsackItem = namedtuple("KnapsackItem", ["weight", "cost", "price", "source_idx"])
BranchNode = namedtuple("BranchNode", ["level", "taken", "bound", "current_weight", "current_cost"])


class BranchAndBoundSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием метода ветвей и границ."""
        items = [
            KnapsackItem(weight, cost, cost / weight, idx)
            for idx, (weight, cost) in enumerate(zip(self.weights, self.costs))
        ]
        items.sort(key=lambda x: x.price, reverse=True)
        
        best_cost = 0
        best_selection = 0
        priority_queue = []

        initial_bound = self._get_bound(0, 0, 0, items)
        initial_node = BranchNode(
            level = 0,
            taken = 0,
            bound = initial_bound,
            current_weight = 0,
            current_cost = 0
        )
        heapq.heappush(priority_queue, (-initial_bound, initial_node))
        
        while priority_queue:
            negative_bound, current_node = heapq.heappop(priority_queue)

            if current_node.bound <= best_cost:
                continue

            if current_node.level == len(items):
                if current_node.current_cost > best_cost:
                    best_cost = current_node.current_cost
                    best_selection = current_node.taken
                continue
            
            current_item = items[current_node.level]

            if current_node.current_weight + current_item.weight <= self.weight_limit:
                new_weight = current_node.current_weight + current_item.weight
                new_cost = current_node.current_cost + current_item.cost
                next_selection = current_node.taken | (1 << current_item.source_idx)
                
                new_bound = self._get_bound(
                    current_node.level + 1,
                    new_weight,
                    new_cost,
                    items
                )
                
                if new_bound > best_cost:
                    new_node = BranchNode(
                        level = current_node.level + 1,
                        taken = next_selection ,
                        bound = new_bound,
                        current_weight = new_weight,
                        current_cost = new_cost
                    )
                    heapq.heappush(priority_queue, (-new_bound, new_node))
            
            new_bound = self._get_bound(
                current_node.level + 1,
                current_node.current_weight,
                current_node.current_cost,
                items
            )
            
            if new_bound > best_cost:
                new_node = BranchNode(
                    level = current_node.level + 1,
                    taken = current_node.taken,
                    bound = new_bound,
                    current_weight = current_node.current_weight,
                    current_cost = current_node.current_cost
                )
                heapq.heappush(priority_queue, (-new_bound, new_node))
        
        result_items = [i for i in range(self.item_cnt) if best_selection & (1 << i)]
        return KnapsackSolution(cost = best_cost, items = result_items)

    def _get_bound(self, level: int, current_weight: int, current_cost: int, items: list) -> float:
        """Вычисляет верхнюю границу для узла."""
        remaining_capacity = self.weight_limit - current_weight
        bound = current_cost
        
        for i in range(level, len(items)):
            if items[i].weight <= remaining_capacity:
                bound += items[i].cost
                remaining_capacity -= items[i].weight
            else:
                bound += items[i].price * remaining_capacity
                break
        
        return bound

if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = BranchAndBoundSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )