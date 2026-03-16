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
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            self._use_brute_force = True
            self._brute_force_solver = BruteForceSolver(weights, costs, weight_limit)
            self.__population = {}
        else:
            self._use_brute_force = False
            self.__population_cnt = min(2**self.item_cnt // 2, POPULATION_LIMIT)
            self.__population = {}
            self.__generation = 0 
        
        self.__history = []

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        population_data = []
        for key in self.__population.keys():
            population_data.append((self.__mask.format(key), self.__population[key]))
        return population_data
    
    @property
    def history(self) -> list[dict]:
        """Возвращает историю поколений.

        :return: Список словарей со статистикой по поколениям.
        """
        return self.__history.copy()

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма.
        
        :param epoch_cnt: Количество поколений для эволюции.
        :return: KnapsackSolution с максимальной стоимостью и индексами предметов.
        """
        if self._use_brute_force:
            return self._brute_force_solver.get_knapsack()

        if self.__generation == 0 and not self.__population:
            self.__population = self.__generate_population(self.__population_cnt)
            self.__save_generation_stats("Начальная популяция")

        for generation in range(epoch_cnt):
            parents = self.__tournament_selection()

            offspring = self.__crossover_population(parents)

            mutated_offspring = []
            for individual in offspring:
                if individual not in self.__population:
                    mutated_offspring.append(individual)
                else:
                    mutated = self.__mutation(individual)
                    if mutated != None:
                        mutated_offspring.append(mutated)

            self.__create_next_generation(mutated_offspring)
            self.__generation += 1
            self.__save_generation_stats(f"Поколение {self.__generation}")

        return self.__get_best_solution()

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        """Генерирует начальную популяцию уникальных случайных особей.

        :param population_cnt: Требуемый размер популяции
        :return: Словарь {особь: фитнес} с уникальными жизнеспособными особями.
        """
        population = {}
        attempts = 0
        max_attempts = 1000
        
        while len(population) < population_cnt and attempts < max_attempts:
            new_individual = rnd.randint(1, (1 << self.item_cnt) - 1)
            
            if new_individual not in population:
                fitness = self.__get_fit(new_individual)
                if fitness > 0:
                    population[new_individual] = fitness
            
            attempts += 1
        
        return population

    def __tournament_selection(self, tournament_size: int = 3) -> list[int]:
        """Турнирный отбор родителей для скрещивания.

        :param tournament_size: Размер турнирной группы.
        :return: Список особей-родителей, отобранных для скрещивания
        """
        parents = []
        population_list = list(self.__population.keys())

        target_parents_count = len(population_list) // 2
        
        for parent in range(target_parents_count):
            tournament = rnd.sample(population_list, 
                                   min(tournament_size, len(population_list)))
            winner = max(tournament, key=lambda x: self.__population[x])
            parents.append(winner)
        
        return parents
    
    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Двухточечное скрещивание двух особей.
        
        :param ancestor1: Первая родительская особь.
        :param ancestor2: Вторая родительская особь.
        :return: Кортеж из двух особей-потомков.
        """
        if self.item_cnt <= 1:
            return ancestor1, ancestor2

        points = sorted(rnd.sample(range(1, self.item_cnt), 2))
        point1, point2 = points

        mask = ((1 << point2) - 1) ^ ((1 << point1) - 1)

        child1 = (ancestor1 & ~mask) | (ancestor2 & mask)
        child2 = (ancestor2 & ~mask) | (ancestor1 & mask)
        
        return child1, child2

    def __crossover_population(self, parents: list[int]) -> list[int]:
        """Выполняет скрещивание для всей популяции родителей.
        
        :param parents: Список особей-родителей.
        :return: Список особей-потомков после скрещивания.
        """
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = self.__cross_items(parents[i], parents[i + 1])
            offspring.append(child1)
            offspring.append(child2)
        
        return offspring
    
    def __mutation(self, item_set: int) -> int | None:
        """Мутация особи.

        :param item_set: Исходная особь для мутации.
        :return: Мутировавшая жизнеспособная особь или None, если мутация неудачна.
        """
        if self.__get_fit(item_set) == 0:
            for attempt in range(10):
                mutated = item_set

                bits_to_clear = rnd.randint(1, min(3, self.item_cnt))
                for item in range(bits_to_clear):
                    bit_pos = rnd.randint(0, self.item_cnt - 1)
                    if mutated & (1 << bit_pos):
                        mutated &= ~(1 << bit_pos)

                if rnd.random() < 0.3:
                    bit_pos = rnd.randint(0, self.item_cnt - 1)
                    mutated |= (1 << bit_pos)

                if self.__get_fit(mutated) > 0:
                    return mutated
            return None

        elif item_set in self.__population:
            for attempt in range(10):
                mutated = item_set

                mutations_count = rnd.randint(1, min(3, self.item_cnt))
                for flip_step in range(mutations_count):
                    bit_pos = rnd.randint(0, self.item_cnt - 1)
                    mutated ^= (1 << bit_pos)

                if self.__get_fit(mutated) > 0:
                    return mutated
            return None
        
        return item_set

    def __create_next_generation(self, offspring: list[int]):
        """Формирует новое поколение на основе потомков.
        
        :param offspring: Список потомков после мутации.
        """
        new_population = {}

        if self.__population:
            sorted_items = sorted(self.__population.items(), 
                                key=lambda x: x[1], reverse=True)
            elite_count = max(1, len(self.__population) // 10)
            for i in range(elite_count):
                ind, fit = sorted_items[i]
                new_population[ind] = fit

        for individual in offspring:
            if individual is None:
                continue
                
            if len(new_population) >= self.__population_cnt:
                break
            
            if individual not in new_population:
                fitness = self.__get_fit(individual)
                if fitness > 0:
                    new_population[individual] = fitness

        attempts = 0
        while len(new_population) < self.__population_cnt and attempts < 1000:
            new_individual = rnd.randint(1, (1 << self.item_cnt) - 1)
            if new_individual not in new_population:
                fitness = self.__get_fit(new_individual)
                if fitness > 0:
                    new_population[new_individual] = fitness
            attempts += 1
        
        self.__population = new_population

    def __get_fit(self, item: int) -> int:
        """Вычисляет фитнес-функцию.
        
        :param item: Особь в виде битовой маски.
        :return: Значение фитнес-функции (стоимость набора предметов).
        """
        weight = 0
        cost = 0
        for i in range(self.item_cnt):
            if item & (1 << i):
                weight += self.weights[i]
                cost += self.costs[i]
        
        return cost if weight <= self.weight_limit else 0

    def __get_best_solution(self) -> KnapsackSolution:
        """Возвращает лучшее решение из текущей популяции.
        
        :return: KnapsackSolution с максимальной стоимостью и индексами предметов.
        """
        if not self.__population:
            return KnapsackSolution(cost=0, items=[])
        
        best_individual = max(self.__population.items(), key=lambda x: x[1])
        best_fitness = best_individual[1]
        best_mask = best_individual[0]
        
        items = [i for i in range(self.item_cnt) if best_mask & (1 << i)]
        return KnapsackSolution(cost=best_fitness, items=items)

    def __save_generation_stats(self, generation_name: str):
        """Сохраняет статистику поколения в историю.
        
        :param generation_name: Название поколения для идентификации в истории.
        """
        if not self.__population:
            return
        
        fitness_values = list(self.__population.values())
        best = max(self.__population.items(), key=lambda x: x[1])
        
        stats = {
            'generation': generation_name,
            'population_size': len(self.__population),
            'best_fitness': best[1],
            'best_individual': self.__mask.format(best[0]),
            'avg_fitness': sum(fitness_values) / len(fitness_values),
            'min_fitness': min(fitness_values),
            'unique_count': len(self.__population)
        }
        self.__history.append(stats)


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
