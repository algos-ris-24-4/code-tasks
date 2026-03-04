import heapq
from collections import namedtuple

from knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

KnapsackItem = namedtuple("KnapsackItem", ["weight", "cost", "price", "source_idx"])
BranchNode = namedtuple("BranchNode", ["level", "taken", "bound"])


class BranchAndBoundSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием метода ветвей и границ."""
        items = [
            KnapsackItem(weight, cost, cost / weight, idx)
            for idx, (weight, cost) in enumerate(zip(self.weights, self.costs))
        ]
        items.sort(key=lambda x: x.price, reverse=True)

        items_count = len(items)
        best_cost = 0
        best_taken = [False] * items_count

        root = BranchNode(
            level=0,
            taken=[],
            bound=self._get_bound(level=0, taken=[], items=items),
        )
        queue = [(-root.bound, root)]

        while queue:
            _, node = heapq.heappop(queue)
            if node.bound <= best_cost:
                continue

            if node.level >= items_count:
                continue

            next_level = node.level + 1
            for take in (True, False):
                new_taken = node.taken + [take]

                current_weight = 0
                current_cost = 0
                for idx, is_taken in enumerate(new_taken):
                    if is_taken:
                        current_weight += items[idx].weight
                        current_cost += items[idx].cost

                if current_weight <= self.weight_limit and current_cost > best_cost:
                    best_cost = current_cost
                    best_taken = new_taken + [False] * (items_count - len(new_taken))

                new_bound = self._get_bound(
                    level=next_level,
                    taken=new_taken,
                    items=items,
                )
                if new_bound > best_cost:
                    branch = BranchNode(
                        level=next_level,
                        taken=new_taken,
                        bound=new_bound,
                    )
                    heapq.heappush(queue, (-new_bound, branch))

        result_items = [
            items[idx].source_idx
            for idx, is_taken in enumerate(best_taken)
            if is_taken
        ]
        result_items.sort()
        return KnapsackSolution(cost=best_cost, items=result_items)

    def _get_bound(self, level, taken, items):
        total_weight = 0
        total_cost = 0

        for idx, is_taken in enumerate(taken):
            if is_taken:
                total_weight += items[idx].weight
                total_cost += items[idx].cost

        if total_weight > self.weight_limit:
            return 0

        for idx in range(level, len(items)):
            item = items[idx]
            if total_weight + item.weight <= self.weight_limit:
                total_weight += item.weight
                total_cost += item.cost
                continue

            remain = self.weight_limit - total_weight
            total_cost += item.price * remain
            break

        return total_cost


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
