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

        if self.item_cnt <= BRUTE_FORCE_BOUND:
            self.__population_cnt = 0
            self.__population = {}
        else:
            self.__population_cnt = min(2**self.item_cnt // 2, POPULATION_LIMIT)
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
            solver = BruteForceSolver(self.weights,self.costs,self.weight_limit)
            return solver.get_knapsack()

        for _ in range(epoch_cnt):
            parents_count = len(self.__population) // 2 
            ancestors_gen_nums = self.__choose_ancestors_for_crossing(parents_count)

            children = self.__cross_population(list(ancestors_gen_nums))

            mut_children = set()

            for child in children:
                if rnd.random() < 0.1:
                    mut_child_chrom = self.__mutation_chrom_wrap(child.chromosome)
                    mut_children.add(Individ(int(mut_child_chrom, 2), mut_child_chrom, self.__get_fit(mut_child_chrom)))
                else: 
                    mut_children.add(child)

            self.__update_population(mut_children, ancestors_gen_nums)

        best_ind = max(self.__population.values(), key=lambda x: x.fitness)
        best_chrom = best_ind.chromosome
        
        result_cost = self.get_cost(self.__get_items_selection_flags(best_chrom))
        result_items_cfg = self.__get_selected_items_idxes(best_chrom)

        return KnapsackSolution(result_cost, result_items_cfg)


    def __get_chromosome(self, number: int) -> str:
        """Преобразует число в бин строку фиксированной длины"""
        return self.__mask.format(number)


    def __get_selected_items_idxes(self, chrom: str) -> list[int]:
        """Возвращает список индексов предметов учтенных в комбинации бин строки"""
        return [item_idx for item_idx in range(len(chrom)) if chrom[item_idx] == '1']


    def __get_items_selection_flags(self, chrom: str) -> list[bool]:
        """Возвращает хромосому в виде списка булевых значений"""
        return [gen == '1' for gen in chrom]


    def __generate_population(self, population_cnt: int) -> dict[int, Individ]:
        """Генерация изначальной-первой популяции"""
        curr_population: dict[int, Individ] = dict()
        
        for _ in range(population_cnt):
            num = rnd.randint(0, 2**self.item_cnt - 1)
            chrom = self.__get_chromosome(num)
            fit = self.__get_fit(chrom)

            while curr_population.get(num) is not None or not(self.__is_individ_valid(chrom)):
                num = rnd.randint(0, 2**self.item_cnt - 1)
                chrom = self.__get_chromosome(num)
                fit = self.__get_fit(chrom)

            curr_population[num] = Individ(num, chrom, fit)

        return curr_population
    

    def __update_population(self, children: list[Individ], ancestors_gen_numbers: set[int]) -> None:
        sorted_individs = sorted(self.__population.values(), key=lambda idv: idv.fitness)         
        removed_individs: set[int] = set() 

        for adding_individ in children:
            removing_individ = None

            if not self.__is_individ_valid(adding_individ.chromosome):
                continue
            if adding_individ.genetic_number in self.__population:
                continue

            for indv in sorted_individs:
                if indv.genetic_number not in ancestors_gen_numbers and indv.genetic_number not in removed_individs:
                    removing_individ = indv
                    break

            if removing_individ is None:
                break

            del self.__population[removing_individ.genetic_number]
            removed_individs.add(removing_individ.genetic_number)
            self.__population[adding_individ.genetic_number] = adding_individ


    def __choose_ancestors_for_crossing(self, ancestors_count: int) -> set[int]:
        """Выбор особей для скрещивания методом рулетки (без дубликатов)."""
        ancestors: set[int] = set()
        total_fitness_sum = sum(idv.fitness for idv in self.__population.values())
        
        max_attempts = ancestors_count * 10
        attempts = 0

        while len(ancestors) < ancestors_count and attempts < max_attempts:
            roulette_choice = rnd.randint(0, total_fitness_sum - 1)
            current_fitness_sum = 0
            
            for idv in self.__population.values():
                current_fitness_sum += idv.fitness
                if roulette_choice < current_fitness_sum:
                    ancestors.add(idv.genetic_number)
                    break
            
            attempts += 1

        return ancestors


    def __cross_population(self, ancestors: list[int]) -> list[Individ]:
        children = []

        for idv_idx in range(0, len(ancestors) - 1, 2):
            anc1 = self.__population[ancestors[idv_idx]]
            anc2 = self.__population[ancestors[idv_idx + 1]]

            child1, child2 = self.__cross_items(anc1, anc2)
            children.append(child1)
            children.append(child2)

        return children


    def __cross_items(self, ancestor1: Individ, ancestor2: Individ) -> tuple[Individ, Individ]:
        """Создание разреза и формирование новых хромосом"""

        cut_point = rnd.randint(1, self.item_cnt - 1)

        child1_chrom = ancestor1.chromosome[:cut_point] + ancestor2.chromosome[cut_point:]
        child2_chrom = ancestor2.chromosome[:cut_point] + ancestor1.chromosome[cut_point:]
        
        if self.__is_need_mutaion(child1_chrom):
            child1_chrom = self.__mutation_chrom_wrap(child1_chrom)

        if self.__is_need_mutaion(child2_chrom):
            child2_chrom = self.__mutation_chrom_wrap(child2_chrom)

        child1 = Individ(int(child1_chrom, 2), child1_chrom, self.__get_fit(child1_chrom))
        child2 = Individ(int(child2_chrom, 2), child2_chrom, self.__get_fit(child2_chrom))

        return (child1, child2)


    def __mutation_chrom(self, chrom: str) -> str:
        chrom_lst = list(chrom)
        mut_point = rnd.randint(0, self.item_cnt - 1)

        if chrom_lst[mut_point] == '0':
            chrom_lst[mut_point] = '1'
        else: 
            chrom_lst[mut_point] = '0'

        return ''.join(chrom_lst)        


    def __is_need_mutaion(self, chrom: str):
        return not(self.__is_individ_valid(chrom)) or self.__population.get(int(chrom, 2)) is not None


    def __mutation_chrom_wrap(self, chrom: str) -> str:
        """Метод мутации хромосомы отдельной особи"""

        new_chrom = self.__mutation_chrom(chrom)
        attempt = 0
        while self.__is_need_mutaion(new_chrom) and attempt < 1000:
            new_chrom = self.__mutation_chrom(chrom)
            attempt += 1
        return new_chrom


    def __is_individ_valid(self, chromosome: str) -> bool:
        return self.get_weight(self.__get_items_selection_flags(chromosome)) <= self.weight_limit


    def __get_fit(self, chromosome: str) -> int:
        return self.get_cost(self.__get_items_selection_flags(chromosome))


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
