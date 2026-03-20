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

PARENT_RATIO = 0.25

MUTATION_RATE = 0.02

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
        if not any(w <= weight_limit for w in weights):
            raise ValueError("Ни один предмет не помещается в рюкзак.")
        self.__mask = "{0:0" + str(len(weights)) + "b}"
        self.__population_cnt = min(2 ** self.item_cnt // 2, POPULATION_LIMIT)
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
            return BruteForceSolver(self.weights, self.costs, self.weight_limit).get_knapsack()

        self.__population = self.__generate_population(self.__population_cnt)

        for _ in range(epoch_cnt):
            ranked = self.__sort_by_fitness()
            parents = self.__select_parents(ranked)
            children = self.__apply_genetic_operators(parents, len(ranked))
            self.__population = self.__form_new_population(children)

        return self.__pick_best_chromosome()

    def __sort_by_fitness(self) -> list[int]:
        return sorted(
            self.__population,
            key=self.__population.__getitem__,
            reverse=True,
        )

    def __select_parents(self, ranked: list[int]) -> list[int]:
        parent_cnt = max(2, int(len(ranked) * PARENT_RATIO))
        return ranked[:parent_cnt]

    def __apply_genetic_operators(self, parents: list[int], children_cnt: int) -> list[int]:
        children: list[int] = []

        while len(children) < children_cnt:
            for idx in range(0, len(parents) - 1, 2):
                child1, child2 = self.__cross_items(parents[idx], parents[idx+1])
                children.append(self.__mutation(child1))
                children.append(self.__mutation(child2))
        return children

    def __form_new_population(self, children: list[int]) -> dict[int, int]:
        merged = dict(self.__population)
        for chromosome in children:
            if chromosome not in merged:
                merged[chromosome] = self.__get_fit(chromosome)
        top = sorted(merged, key=merged.__getitem__, reverse=True)
        return {chromosome: merged[chromosome] for chromosome in top[:self.__population_cnt]}

    def __pick_best_chromosome(self) -> KnapsackSolution:
        best = max(self.__population, key=self.__population.__getitem__)
        best_cost = self.__population[best]
        items = [i for i in range(self.item_cnt) if best & (1 << (self.item_cnt - 1 - i))]
        return KnapsackSolution(best_cost, items)

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        population: dict[int, int] = {}
        while len(population) < population_cnt:
            chromosome = rnd.getrandbits(self.item_cnt)
            if chromosome not in population:
                population[chromosome] = self.__get_fit(chromosome)
        return population

    def __cross_items(self, parent1: int, parent2: int) -> tuple[int, int]:
        child1, child2 = 0, 0
        for bit in range(self.item_cnt):
            if rnd.randint(0, 1):
                child1 |= parent1 & (1 << bit)
                child2 |= parent2 & (1 << bit)
            else:
                child1 |= parent2 & (1 << bit)
                child2 |= parent1 & (1 << bit)
        return child1, child2

    def __mutation(self, item_set: int) -> int:
        for bit in range(self.item_cnt):
            if rnd.random() < MUTATION_RATE:
                item_set ^= 1 << bit
        return item_set

    def __get_fit(self, item: int) -> int:
        total_weight = 0
        total_cost = 0
        for i in range(self.item_cnt):
            if item & (1 << (self.item_cnt - 1 - i)):
                total_weight += self.weights[i]
                if total_weight > self.weight_limit:
                    return 0
                total_cost += self.costs[i]
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