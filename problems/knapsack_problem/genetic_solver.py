import random as rnd

from collections import namedtuple

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


Individ = namedtuple("Individ", ["genetic_number", "chromosome", "fitness"]);

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
        for idv in self.__population.values():
            population_data.append((idv.chromosome, idv.fitness))
        return population_data


    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""

        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BruteForceSolver.get_knapsack()

        for _ in range(EPOCH_CNT):
            # отбор родителей
            ancestors_gen_nums = self.__choose_ancestors_for_crossing(...)  # TODO: добавить вычисление количества родителей

            # применить скрещивание / мутацию
            children = ...

            # mutation???
            ...

            # обновить популяцию
            self.__update_population(children, ancestors_gen_nums)

        
        # выбрать лучшую хромосому /////// TODO: ВОЗМОЖНО СТОИТ ХРАНИТЬ ТЕКУЩЕГО ЛИДЕРА
        best_chrom = ...
        
        # вернуть ответ
        result_cost = self.get_cost(self.__get_items_selection_flags(best_chrom))
        result_items_cfg = self.__get_selected_items_idxes(best_chrom)

        return KnapsackSolution(result_cost, result_items_cfg)


    def __get_chromosome(self, number: int) -> str:
        return self.__mask.format(number)


    def __get_selected_items_idxes(self, chrom: str) -> list[int]:
        return [item_idx for item_idx in len(chrom) if chrom[item_idx] == '1']


    def __get_items_selection_flags(self, chrom: str) -> list[bool]:
        return [gen == '1' for gen in chrom]


    def __generate_population(self, population_cnt: int) -> dict[int, Individ]:
        curr_population: dict[int, int] = dict()
        
        for _ in range(population_cnt):
            chrom = self.__get_chromosome(num)
            fit = self.__get_fit(chrom)

            while curr_population.get(num) != None or fit > self.weight_limit:
                num = rnd.randint(1, len(self.item_cnt))
                chrom = self.__get_chromosome(num)
                fit = self.__get_fit(chrom)

            curr_population[num] = Individ(num, chrom, fit)

        return curr_population
    

    def __update_population(self, children: list[Individ], ancestors_gen_numbers: set[int]) -> None:
        # TODO: подумать над дубликатами и ухудшением 
        
        sorted_individs = sorted(self.__population.values(), key=lambda idv: idv.fitness)

        removing_idv_idx = 0
        for adding_individ in children:
            
            removing_individ = sorted_individs[removing_idv_idx]
            while removing_individ.genetic_number in ancestors_gen_numbers:
                removing_idv_idx += 1
                removing_individ = sorted_individs[removing_idv_idx]

            del self.__population[removing_individ.genetic_number]
            self.__population[adding_individ.genetic_number] = adding_individ

            removing_idv_idx += 1


    def __choose_ancestors_for_crossing(self, ancestors_count: int) -> set[int]:
        ancestors = set()

        total_fitness_sum = sum(idv.fitness for idv in self.__population.values())
        
        while len(ancestors) < ancestors_count:
            roulette_choice = rnd.randint(0, total_fitness_sum - 1)
            
            current_fitness_sum = 0
            for idv in self.__population.values():
                current_fitness_sum += idv.fitness
                if roulette_choice <= current_fitness_sum:
                    ancestors.add(idv.genetic_number)
                    break

        return ancestors


    def __cross_population(self, ancestors: list[int]) -> list[Individ]:
        children = []

        for idv_idx in range(0, len(ancestors) - 1, 2):
            anc1 = self.__population[ancestors[idv_idx]]
            anc2 = self.__population[ancestors[idv_idx + 1]]

            child1, child2 = self.__cross_items(self, anc1, anc2)
            children.append(child1)
            children.append(child2)

        return children



    def __cross_items(self, ancestor1: Individ, ancestor2: Individ) -> tuple[Individ, Individ]:
        pass


    def __mutation(self, item_set: Individ) -> Individ:
        pass


    def __get_fit(self, chromosome: str) -> int:
        return self.get_weight(self.__get_items_selection_flags(chromosome))


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
