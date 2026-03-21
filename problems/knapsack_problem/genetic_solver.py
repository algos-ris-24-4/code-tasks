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
        self.__population_cnt = min(2**self.item_cnt / 2, POPULATION_LIMIT)
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
            bf_solver = BruteForceSolver(self.weights, self.costs, self.weight_limit)
            return bf_solver.get_knapsack()

        population_cnt = int(self.__population_cnt)
        if population_cnt < 2:
            population_cnt = 2

        for _ in range(epoch_cnt):
            masks = list(self.__population.keys())
            fitnesses = list(self.__population.values())

            total_fit = sum(fitnesses)
            selection_weights = fitnesses

            next_generation = {}

            best_mask = max(self.__population, key=self.__population.get)
            best_cost = self.__population[best_mask]
            next_generation[best_mask] = best_cost

            while len(next_generation) < population_cnt:
                parent1, parent2 = rnd.choices(masks, weights=selection_weights, k=2)
                child1, child2 = self.__cross_items(parent1, parent2)

                for child in [child1, child2]:
                    if len(next_generation) < population_cnt:
                        mutated_child = self.__mutation(child)
                        child_fit = self.__get_fit(mutated_child)
                        if child_fit > 0 and mutated_child not in next_generation:
                            next_generation[mutated_child] = child_fit

            self.__population = next_generation

        best_mask = max(self.__population, key=self.__population.get)
        best_cost = self.__population[best_mask]

        bits = self.__mask.format(best_mask)
        items = [idx for idx, bit in enumerate(bits) if bit == '1']

        return KnapsackSolution(cost=best_cost, items=items)

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        pop = {}
        max_val = 2**self.item_cnt - 1
        while len(pop) < population_cnt:
            mask = rnd.randint(0, max_val)
            fit = self.__get_fit(mask)
            if fit > 0 and mask not in pop: # Только те, кто влез по весу
                pop[mask] = fit
        return pop

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        if self.item_cnt < 2:
            return ancestor1, ancestor2
            
        point = rnd.randint(1, self.item_cnt - 1)
        s1 = self.__mask.format(ancestor1)
        s2 = self.__mask.format(ancestor2)
        
        child1_str = s1[:point] + s2[point:]
        child2_str = s2[:point] + s1[point:]
        
        return int(child1_str, 2), int(child2_str, 2)

    def __mutation(self, item_set: int) -> int:
        bit_to_flip = rnd.randint(0, self.item_cnt - 1)
        return item_set ^ (1 << bit_to_flip)

    def __get_fit(self, item):
        bits = self.__mask.format(item)
        selected = [char == '1' for char in bits]
        return self.get_cost(selected) 


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
