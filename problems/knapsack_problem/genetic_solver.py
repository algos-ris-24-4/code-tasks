import random as rnd
import time as time

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

Statistics = namedtuple("Statistics", ["population_cnt", "leader", "time", "std", "dispersion", "sx", "costs_curve" ])

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
        rnd.seed(67)
        super().__init__(weights, costs, weight_limit)
        self.__mask = "{0:0" + str(len(weights)) + "b}"
        self.__population_cnt = int(min(2**self.item_cnt / 2, POPULATION_LIMIT))

        is_low_diversity = False
        diversity = 0

        std = sum(weights) / len(weights)
        d = sum([i ** 2 for i in weights]) / len(weights) - std ** 2
        s = d ** (1/2)

        std_min = std - s
        diversity = int(weight_limit / std_min)

        is_low_diversity = diversity >= 3

        self.__population = self.__generate_population(self.__population_cnt) if is_low_diversity else self.__generate_population_diversity(diversity)
        self.duration_fit = 0

    def get_statistics(self):
        size_population = len(self.population)
        leader = sorted(self.population)[0]
        std = sum([i[1] for i in self.population]) / len(self.population)
        d = sum([i[1] ** 2 for i in self.population]) / len(self.population) - std ** 2
        sx = d ** (1/2)
        costs_curve = [i[1] for i in self.population]
        time = self.duration_fit
        return Statistics(size_population,leader,time,std,d,sx,costs_curve)


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
        current_epoch = 0
        is_small = False
        last_leader = ('', -1)
        same_leader_epoch = 0
        start_timer = time.time()
        while current_epoch < epoch_cnt and same_leader_epoch < 50:
            if len(self.population) < int(self.__population_cnt * 0.5):
                is_small = True
            else:
                is_small = False
            new_population = self.__step_one_form_new_population(is_small)
            current_leader = self.__step_two_clean_population(new_population)
            self.__random_mutations()
            if current_leader[0] != last_leader[0] and current_leader[1] != last_leader[1]:
                last_leader = current_leader
                same_leader_epoch = 0
            same_leader_epoch += 1
            current_epoch += 1

        solution = self.__get_solution_from_population()
        
        result_items = []
        index = 0
        for i in solution[0]:
            if(i == "1"):
                result_items.append(index)
            index += 1 

        self.duration_fit = start_timer - time.time()
        return KnapsackSolution(solution[1], result_items)
    
    def __generate_population_diversity(self, max_items: int) -> dict[int, int]:
        """
        Генерирует все возможные комбинации из 1..int(max_items) предметов,
        которые помещаются в рюкзак по весу.
        Возвращает словарь {маска: стоимость}.
        """
        from itertools import combinations
        k_max = int(max_items)
        if k_max < 1:
            return {}
        population = {}
        for k in range(1, min(k_max, self.item_cnt) + 1):
            for combo in combinations(range(self.item_cnt), k):
                total_weight = sum(self.weights[i] for i in combo)
                if total_weight <= self.weight_limit:
                    mask = 0
                    total_cost = 0
                    for i in combo:
                        mask |= 1 << i
                        total_cost += self.costs[i]
                    population[mask] = total_cost
        return population
    def __step_one_form_new_population(self, parent_choose_method: bool):
        """Первый шаг генетического алгоритма: Формирование нового поколения."""
        sorted_population = sorted(self.population, key=lambda x: x[1], reverse=True)

        if parent_choose_method:
            parents_list = sorted_population[0:int((len(sorted_population)*0.4))]
        else:
            parents_list = sorted_population[0:int((len(sorted_population)*0.2))] + sorted_population[int((len(sorted_population) * 0.8)):]

        children_list = []
        while len(parents_list) >= 2:
            idx1 = rnd.randint(0, len(parents_list) - 1)
            parent1 = parents_list.pop(idx1)
            idx2 = rnd.randint(0, len(parents_list) - 1)
            parent2 = parents_list.pop(idx2)
            children_list += self.__cross_items(parent1, parent2)
        all_population = sorted_population + children_list
        return all_population
    
    def __step_two_clean_population(self, all_population: list):
        """Второй шаг генетического алгоритма: Ранжирование поколения."""
        all_population = sorted(all_population, key=lambda x: x[1], reverse=True)
        self.__cut_population_excess(all_population)        
        #if len(self.__population) < self.__population_cnt:
        #    self.__add_random_individuals(self.__population_cnt - len(self.__population))
        return all_population[0]
    
    def __random_mutations(self):
        """Случайные мутации популяции."""
        if len(self.__population) > 0:
            max_mutations = max(1, len(self.__population) // 2)
            count_mutation = rnd.randint(1, min(int(self.__population_cnt * 0.2) + 1, max_mutations))
            count_mutation = min(count_mutation, len(self.__population))
            
            mutation_keys = rnd.sample(list(self.__population.keys()), count_mutation)
            for key in mutation_keys:
                mutated = self.__mutation(key)
                if mutated != key:
                    if mutated not in self.__population:
                        fitness = self.__get_fit(mutated)
                        if self.__check_vitals(mutated):
                            self.__population[mutated] = fitness
                            del self.__population[key]
        pass

    def __add_random_individuals(self, needed: int):
        """Генерирует нужное количество случайных допустимых особей и добавляет в популяцию."""
        added = 0
        attempts = 0
        max_attempts = 1000 * self.item_cnt
        while added < needed and attempts < max_attempts:
            new_individual = rnd.randint(1, (1 << self.item_cnt) - 1)
            if new_individual not in self.__population:
                fitness = self.__get_fit(new_individual)
                if self.__check_vitals(new_individual):
                    self.__population[new_individual] = fitness
                    added += 1
            attempts += 1

    
    def __get_solution_from_population(self):
        """Извлекает лучшего индивида из популяции и выдает его в качестве."""
        sorted_population = sorted(self.population, key=lambda x: x[1], reverse=True)
        return sorted_population[0]
    
    def __cut_population_excess(self, sorted_population: list):
        """Меняет внутреннее свойство популяции."""
        self.__population = {}
        count = 0
        for item in sorted_population:
            if count >= self.__population_cnt:
                break
            key = int(item[0], 2)
            self.__population[key] = item[1]
            count += 1

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        """Инициализирует популяцию."""
        population = {}
        attempts = 0
        max_attempts = 1000 * self.item_cnt                
        while len(population) < population_cnt and attempts < max_attempts:
            new_individual = rnd.randint(1, (1 << self.item_cnt) - 1)
            
            if new_individual not in population:
                fitness = self.__get_fit(new_individual)
                if self.__check_vitals(new_individual):
                    population[new_individual] = fitness            
            attempts += 1
        
        return population


    def __cross_items(self, ancestor1: tuple, ancestor2: tuple) -> list[tuple]:
        """"Скрещивает родителей одноточечным методом, где выбор точки случайный и методом последовательного взятия генов у каждого из родителей."""
        children = []

        mask_ancestor1 = ancestor1[0]
        mask_ancestor2 = ancestor2[0]
        position = 0
        buffer_child1 = ""
        buffer_child2 = ""

        while position < len(mask_ancestor1):
            if position % 2 == 0:
                buffer_child1 += mask_ancestor1[position]
                buffer_child2 += mask_ancestor2[position]
            else:
                buffer_child1 += mask_ancestor2[position]
                buffer_child2 += mask_ancestor1[position]
            position += 1

        children.append((buffer_child1, buffer_child2))

        position = 0
        pivot = rnd.randint(1, self.item_cnt - 1)
        buffer_child1 = mask_ancestor1[0:pivot] + mask_ancestor2[pivot:]
        buffer_child2 = mask_ancestor2[0:pivot] + mask_ancestor1[pivot:]
        
        children.append((buffer_child1, buffer_child2))

        result = []
        for child_pair in children:
            for child_mask in child_pair:
                child_int = int(child_mask, 2)
                if self.__check_vitals(child_int):
                    fitness = self.__get_fit(child_int)
                    result.append((child_mask, fitness))

        return result

    def __mutation(self, item_set: int) -> int:  
        """Применяет мутацию на индивида"""      
        attempts = 0
        max_attempts = 1000 * self.item_cnt    
        item_mask = list(self.__mask.format(item_set))
        while attempts < max_attempts:
            mut_index = rnd.randint(0, int(self.item_cnt - 1))
            
            item_mask[mut_index] = '1' if item_mask[mut_index] == '0' else '0'
            
            mutated_int = int(''.join(item_mask), 2)
            if self.__check_vitals(mutated_int):
                return mutated_int

            attempts += 1
        return item_set

    def __get_fit(self, item: int):
        """Фитнесс-функция."""
        mask_item = self.__mask.format(item)
        current_item = 0
        total_cost = 0
        total_weight = 0
        while current_item < len(mask_item):
            if mask_item[current_item] == '1':
                total_cost += self.costs[current_item]
                total_weight += self.weights[current_item]
            current_item += 1
        if total_weight <= self.weight_limit:
            return total_cost
        
        return 0

    def __check_vitals(self, item: int):
        """Проверяет, является ли особь жизнеспособной."""
        mask_item = self.__mask.format(item)
        current_item = 0
        total_weight = 0
        while current_item < len(mask_item):
            if mask_item[current_item] == '1':
                total_weight += self.weights[current_item]
            current_item += 1
        return total_weight <= self.weight_limit

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