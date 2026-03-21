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
            ancestors_gen_nums = self.__choose_ancestors_for_crossing(parents_count)  # TODO: добавить вычисление количества родителей

            children = self.__cross_population(list(ancestors_gen_nums))

            mut_children = []
            for child in children:
                if rnd.random() < 0.1:
                    mut_children.append(self.__mutation(child))
                else: mut_children.append(child)

            self.__update_population(mut_children, ancestors_gen_nums)

        # Лучшая особь в популяции и лучшая хромосома
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

            while curr_population.get(num) != None or self.get_weight(
                self.__get_items_selection_flags(chrom)) > self.weight_limit:
                num = rnd.randint(0, 2**self.item_cnt - 1)
                chrom = self.__get_chromosome(num)
                fit = self.__get_fit(chrom)

            curr_population[num] = Individ(num, chrom, fit)

        return curr_population
    

    def __update_population(self, children: list[Individ], ancestors_gen_numbers: set[int]) -> None:
        
        
        for adding_individ in children:

            if adding_individ.genetic_number in self.__population:
                adding_individ = self.__mutation(adding_individ)
            
                for _ in range(3):
                    if adding_individ.genetic_number in self.__population:
                        adding_individ = self.__mutation(adding_individ)
                    else:
                        break
                            
            sorted_individs = sorted(self.__population.values(), key=lambda idv: idv.fitness)              
            removing_individ = None
            for indv in sorted_individs:
                if indv.genetic_number not in ancestors_gen_numbers:
                    removing_individ = indv
                    break
            if removing_individ is None:
                break

            del self.__population[removing_individ.genetic_number]
            self.__population[adding_individ.genetic_number] = adding_individ



    def __choose_ancestors_for_crossing(self, ancestors_count: int) -> set[int]:
        ancestors = set()

        total_fitness_sum = sum(idv.fitness for idv in self.__population.values())

        if total_fitness_sum == 0:
            numbers = list(self.__population.keys())
            needed = min(ancestors_count, len(numbers))
            while len(ancestors) < needed:
                ancestors.add(rnd.choice(numbers))
            return ancestors
        
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

            child1, child2 = self.__cross_items(anc1, anc2)
            children.append(child1)
            children.append(child2)

        return children



    def __cross_items(self, ancestor1: Individ, ancestor2: Individ) -> tuple[Individ, Individ]:
        """Создание разреза и формирование новых хромосом"""

        cut_point = rnd.randint(1, self.item_cnt-1)

        child1_chrom = ancestor1.chromosome[:cut_point] + ancestor2.chromosome[cut_point:]
        child2_chrom = ancestor2.chromosome[:cut_point] + ancestor1.chromosome[cut_point:]
        
        child1_num = int(child1_chrom, 2)
        child2_num = int(child2_chrom, 2)
        child1_fit = self.__get_fit(child1_chrom)
        child2_fit = self.__get_fit(child2_chrom)

        return (
            Individ(child1_num,child1_chrom,child1_fit),
            Individ(child2_num,child2_chrom,child2_fit)
        )


    def __mutation(self, item_set: Individ) -> Individ:
        """Метод мутации хромосомы отдельной особи"""

        chrom = list(item_set.chromosome)

        mut_point = rnd.randint(0, self.item_cnt -1)

        if chrom[mut_point] == '0':
            chrom[mut_point] = '1'
        else: 
            chrom[mut_point] = '0'

        new_chrom = ''.join(chrom)
        new_num_mut_chrom = int(new_chrom, 2)
        new_fit_mut_chrom = self.__get_fit(new_chrom)

        return Individ(new_num_mut_chrom,new_chrom,new_fit_mut_chrom)


    def __get_fit(self, chromosome: str) -> int:
        current = self.__get_items_selection_flags(chromosome)
        if self.get_weight(current) > self.weight_limit:
            return 0
        else: return self.get_cost(current)


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
