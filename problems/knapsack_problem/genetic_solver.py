import random as rnd
import time

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

POPULATION_LIMIT = 1000
EPOCH_CNT = 100
BRUTE_FORCE_BOUND = 5
TIME_LIMIT = 10

class GeneticSolver(KnapsackAbstractSolver):
    """Класс для решения задачи о рюкзаке с использованием генетического алгоритма."""

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int):
        super().__init__(weights, costs, weight_limit)
        self.__mask = "{0:0" + str(len(weights)) + "b}"
        self.__population_cnt = min(2**self.item_cnt // 2, POPULATION_LIMIT)
        self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции."""
        population_data = []
        for key in self.__population.keys():
            population_data.append((self.__mask.format(key), self.__population[key]))
        return population_data

    def get_knapsack(self, epoch_cnt=EPOCH_CNT, time_limit_sec: float | None = None) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""
        
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BranchAndBoundSolver(self.weights, self.costs, self.weight_limit).get_knapsack()

        population_cnt = self.__population_cnt
        start_time = time.perf_counter()

        if time_limit_sec is not None and time_limit_sec <= 0:
            best_item, best_fit = max(self.__population.items(), key=lambda item: item[1])
            return KnapsackSolution(
                cost=best_fit,
                items=[idx for idx in range(self.item_cnt) if best_item & (1 << (self.item_cnt - 1 - idx))],
            )

        for _ in range(int(epoch_cnt)):
            if time_limit_sec is not None and time.perf_counter() - start_time >= time_limit_sec:
                break

            sorted_population = sorted(
                self.__population.items(), key=lambda item: item[1], reverse=True
            )
            
            parent_cnt = max(2, len(sorted_population) // 2)
            parents = [item for item, _ in sorted_population[:parent_cnt]]
            rnd.shuffle(parents)

            progeny: dict[int, int] = {}
            for i in range(0, len(parents) - 1, 2):
                if i + 1 >= len(parents):
                    break
                child1, child2 = self.__cross_items(parents[i], parents[i + 1])
                
                for child in (child1, child2):
                    for _ in range(self.item_cnt):
                        if time_limit_sec is not None and time.perf_counter() - start_time >= time_limit_sec:
                            break
                            
                        fit = self.__get_fit(child)
                        is_duplicate = child in self.__population or child in progeny
                        if fit > 0 and not is_duplicate:
                            progeny[child] = fit
                            break
                        child = self.__mutation(child)
                    
                    if time_limit_sec is not None and time.perf_counter() - start_time >= time_limit_sec:
                        break

            combined = {**self.__population, **progeny}
            sorted_combined = sorted(combined.items(), key=lambda x: x[1], reverse=True)
            self.__population = dict(sorted_combined[:population_cnt])

        best_item, best_fit = max(self.__population.items(), key=lambda item: item[1])
        return KnapsackSolution(
            cost=best_fit,
            items=[idx for idx in range(self.item_cnt) if best_item & (1 << (self.item_cnt - 1 - idx))],
    )

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        population_limit = int(population_cnt)
        max_mask_value = (1 << self.item_cnt) - 1
        population: dict[int, int] = {}

        ranked_items = list(range(self.item_cnt))
        ranked_items.sort(key=lambda i: self.costs[i] / self.weights[i], reverse=True)

        selected = [False] * self.item_cnt
        current_weight = 0
        for idx in ranked_items:
            if current_weight + self.weights[idx] <= self.weight_limit:
                selected[idx] = True
                current_weight += self.weights[idx]
                bits = "".join("1" if flag else "0" for flag in selected)
                item_set = int(bits, 2)
                fit = self.__get_fit(item_set)
                if fit > 0:
                    population[item_set] = fit
                if len(population) >= population_limit:
                    return population

        if max_mask_value <= 10 * population_limit:
            for item_set in range(1, max_mask_value + 1):
                fit = self.__get_fit(item_set)
                if fit > 0:
                    population[item_set] = fit
                if len(population) >= population_limit:
                    break
            if len(population) >= 2:
                return population

        random_gen_attempt_limit = population_limit * 50
        attempts = 0
        for _ in range(random_gen_attempt_limit):
            if len(population) >= population_limit:
                break
            item_set = rnd.randint(1, max_mask_value)
            if item_set in population:
                continue
            fit = self.__get_fit(item_set)
            if fit > 0:
                population[item_set] = fit
            attempts += 1

        if len(population) < 2:
            for item_idx in range(self.item_cnt):
                item_set = 1 << (self.item_cnt - 1 - item_idx)
                fit = self.__get_fit(item_set)
                if fit > 0 and item_set not in population:
                    population[item_set] = fit
                if len(population) >= 2:
                    break

        fill_attempts = 0
        final_population_fill_limit = population_limit * 50
        while len(population) < population_limit and fill_attempts < final_population_fill_limit:
            item_set = rnd.randint(0, max_mask_value)
            if item_set not in population:
                population[item_set] = self.__get_fit(item_set)
            fill_attempts += 1

        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        n = self.item_cnt
        crossover_point = max(1, min(n - 1, n // 2))
        right_part_len = n - crossover_point
        right_bits_mask = (1 << right_part_len) - 1
        left_bits_mask = ((1 << n) - 1) ^ right_bits_mask
        child1 = (ancestor1 & left_bits_mask) | (ancestor2 & right_bits_mask)
        child2 = (ancestor2 & left_bits_mask) | (ancestor1 & right_bits_mask)
        return child1, child2

    def __mutation(self, item_set: int) -> int:
        n = self.item_cnt
        item_idx = rnd.randint(0, n - 1)
        bit_pos = (n - 1) - item_idx
        return item_set ^ (1 << bit_pos)

    def __get_fit(self, item):
        n = self.item_cnt
        x = item
        total_weight = 0
        total_cost = 0
        for i in range(n - 1, -1, -1):
            if x & 1:
                total_weight += self.weights[i]
                if total_weight > self.weight_limit:
                    return 0
                total_cost += self.costs[i]
            x >>= 1
        return total_cost


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов: {weights}")
    print(f"Стоимости предметов: {costs}")
    print(f"Ограничение вместимости: {weight_limit}")
    
    solver = GeneticSolver(weights, costs, weight_limit)
    result = solver.get_knapsack(epoch_cnt=100, time_limit_sec=TIME_LIMIT)
    print(f"Максимальная стоимость: {result.cost}, индексы предметов: {result.items}")