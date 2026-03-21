import heapq
import random as rnd

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

POPULATION_LIMIT = 1000
"""Предельный размер популяции."""

EPOCH_CNT = 100
"""Количество поколений по умолчанию."""

BRUTE_FORCE_BOUND = 5
"""Размер входных данных задачи, до которого используется полный перебор."""


class GeneticSolver(KnapsackAbstractSolver):
    """Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный
    перебор.

    Экземпляр класса хранит состояние популяции, метод поиска решения может
    быть запущен многократно для одного экземпляра.

    """

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int):
        """Создает объект класса для решения задачи о рюкзаке.

        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
        """
        super().__init__(weights, costs, weight_limit)
        self.__mask = "{0:0" + str(len(weights)) + "b}"
        self.__population_cnt = min(2 ** self.item_cnt / 2, POPULATION_LIMIT)
        self.__fit_cache: dict[int, int] = {}
        self.__weight_cache: dict[int, int] = {}
        self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        population_data = []
        for key in self.__population.keys():
            population_data.append((self.__mask.format(key), self.__population[key]))
        return population_data

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BruteForceSolver(
                self._weights, self._costs, self._weight_limit
            ).get_knapsack()

        pop_size = int(self.__population_cnt)

        for _ in range(epoch_cnt):
            parent_cnt = max(2, len(self.__population) // 2)
            top = heapq.nlargest(parent_cnt, self.__population.items(), key=lambda x: x[1])
            parents = [item_set for item_set, _ in top]
            rnd.shuffle(parents)

            offspring: dict[int, int] = {}
            for i in range(0, len(parents) - 1, 2):
                child1, child2 = self.__cross_items(parents[i], parents[i + 1])
                for child in (child1, child2):
                    for _ in range(5):
                        if child == 0:
                            child = self.__mutation(child)
                            continue
                        fit = self.__get_fit(child)
                        is_duplicate = child in self.__population or child in offspring
                        if fit > 0 and not is_duplicate:
                            offspring[child] = fit
                            break
                        child = self.__mutation(child)

            combined = {**self.__population, **offspring}
            self.__population = dict(
                heapq.nlargest(pop_size, combined.items(), key=lambda x: x[1])
            )

        best_item, best_fit = max(self.__population.items(), key=lambda x: x[1])
        items = [
            i for i in range(self.item_cnt)
            if best_item & (1 << (self.item_cnt - 1 - i))
        ]
        return KnapsackSolution(cost=best_fit, items=items)

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        """Создаёт начальную популяцию случайных валидных особей."""
        population: dict[int, int] = {}
        max_item = (1 << self.item_cnt) - 1

        if max_item < 4 * POPULATION_LIMIT:
            for item_set in range(1, max_item + 1):
                fit = self.__get_fit(item_set)
                if fit > 0:
                    population[item_set] = fit
            return population

        max_attempts = int(population_cnt) * 20
        for _ in range(max_attempts):
            if len(population) >= population_cnt:
                break
            item_set = rnd.randint(1, max_item)
            if item_set not in population:
                fit = self.__get_fit(item_set)
                if fit > 0:
                    population[item_set] = fit

        if len(population) < 2:
            for i in range(self.item_cnt):
                item_set = 1 << i
                fit = self.__get_fit(item_set)
                if fit > 0 and item_set not in population:
                    population[item_set] = fit

        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Равномерное скрещивание: случайная маска определяет, чьи биты куда идут."""
        all_bits = (1 << self.item_cnt) - 1
        cross_mask = rnd.randint(0, all_bits)
        inv_mask = (~cross_mask) & all_bits

        child1 = (ancestor1 & cross_mask) | (ancestor2 & inv_mask)
        child2 = (ancestor2 & cross_mask) | (ancestor1 & inv_mask)
        return child1, child2

    def __mutation(self, item_set: int) -> int:
        """Мутация: инвертирует один случайный бит особи."""
        bit_pos = rnd.randint(0, self.item_cnt - 1)
        mutated = item_set ^ (1 << bit_pos)
        if item_set in self.__weight_cache:
            old_weight = self.__weight_cache[item_set]
            item_idx = self.item_cnt - 1 - bit_pos
            if mutated & (1 << bit_pos):
                self.__weight_cache[mutated] = old_weight + self._weights[item_idx]
            else:
                self.__weight_cache[mutated] = old_weight - self._weights[item_idx]
        return mutated

    def __get_fit(self, item_set: int) -> int:
        """Фитнес-функция: стоимость набора, если вес не превышает лимит, иначе 0."""
        if item_set in self.__fit_cache:
            return self.__fit_cache[item_set]
        weights = self._weights
        costs = self._costs
        limit = self._weight_limit

        if item_set in self.__weight_cache:
            total_weight = self.__weight_cache[item_set]
            if total_weight > limit:
                self.__fit_cache[item_set] = 0
                return 0
            total_cost = 0
            tmp = item_set
            i = self.item_cnt - 1
            while tmp:
                if tmp & 1:
                    total_cost += costs[i]
                tmp >>= 1
                i -= 1
            self.__fit_cache[item_set] = total_cost
            return total_cost
        
        total_weight = 0
        total_cost = 0
        tmp = item_set
        i = self.item_cnt - 1
        while tmp:
            if tmp & 1:
                total_weight += weights[i]
                if total_weight > limit:
                    self.__fit_cache[item_set] = 0
                    return 0
                total_cost += costs[i]
            tmp >>= 1
            i -= 1
        self.__weight_cache[item_set] = total_weight
        self.__fit_cache[item_set] = total_cost
        return total_cost


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = GeneticSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
