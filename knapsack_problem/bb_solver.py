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

        n = len(items)
        best_cost = 0
        best_taken = [False] * n
        priority_queue = []

        initial_taken = [False] * n
        root_bound = self._get_bound(-1, initial_taken, items)
        root_node = BranchNode(level=-1, taken=initial_taken, bound=root_bound)
        heapq.heappush(priority_queue, (-root_bound, -1, root_node))

        while priority_queue:
            _, _, node = heapq.heappop(priority_queue)

            if node.bound <= best_cost:
                continue

            current_level = node.level
            current_taken = node.taken
            next_level = current_level + 1

            if next_level == n:
                current_cost = 0
                for i, is_taken in enumerate(current_taken):
                    if is_taken:
                        current_cost += items[i].cost
                if current_cost > best_cost:
                    best_cost = current_cost
                    best_taken = current_taken[:]
                continue

            item = items[next_level]
            current_weight = 0
            for i, is_taken in enumerate(current_taken):
                if is_taken:
                    current_weight += items[i].weight

            if current_weight + item.weight <= self.weight_limit:
                new_taken_take = current_taken[:]
                new_taken_take[next_level] = True
                bound_take = self._get_bound(next_level, new_taken_take, items)
                if bound_take > best_cost:
                    new_node_take = BranchNode(
                        level=next_level,
                        taken=new_taken_take,
                        bound=bound_take
                    )
                    heapq.heappush(priority_queue, (-bound_take, -next_level, new_node_take))

            new_taken_skip = current_taken[:]
            new_taken_skip[next_level] = False
            bound_skip = self._get_bound(next_level, new_taken_skip, items)
            if bound_skip > best_cost:
                new_node_skip = BranchNode(
                    level=next_level,
                    taken=new_taken_skip,
                    bound=bound_skip
                )
                heapq.heappush(priority_queue, (-bound_skip, -next_level, new_node_skip))

        final_indices = []
        for i in range(n):
            if best_taken[i]:
                final_indices.append(items[i].source_idx)

        return KnapsackSolution(cost=best_cost, items=final_indices)

    def _get_bound(self, level, taken, items):
        current_weight = 0
        current_cost = 0.0
        n = len(items)

        for i in range(level + 1):
            if taken[i]:
                current_weight += items[i].weight
                current_cost += items[i].cost

        if current_weight > self.weight_limit:
            return 0.0

        remaining_space = self.weight_limit - current_weight

        for i in range(level + 1, n):
            item = items[i]
            if item.weight <= remaining_space:
                current_weight += item.weight
                current_cost += item.cost
                remaining_space -= item.weight
            else:
                fraction = remaining_space / item.weight
                current_cost += item.cost * fraction
                break

        return current_cost


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