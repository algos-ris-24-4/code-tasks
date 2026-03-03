from math import inf

from network_flow.max_flow_calculator import MaxFlowCalculator
from network_flow.network_validator import NetworkValidator
from shortest_path.bellman_ford import (
    NegativeLoopBellmanFordError,
    bellman_ford,
    restore_path,
)
from shortest_path.floyd_warshall import NegativeLoopFloydWarshallError, floyd_warshall

COST_MATRIX_NAME = "Таблица стоимости транспортировки"


class MinCostFlowCalculator(MaxFlowCalculator):
    """Класс для решения задачи поиска максимального потока минимальной стоимости"""

    def __init__(self, capacity_matrix: list[list[int]], cost_matrix: list[list[int]]):
        """
        Конструктор класса.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        :param cost_matrix: Квадратная матрица стоимости транспортировки.
        :type cost_matrix: list[list[int]]
        """
        NetworkValidator.validate_matrix(cost_matrix, COST_MATRIX_NAME)
        super().__init__(capacity_matrix)

        self._cost_matrix = cost_matrix
        self._residual_matrix, self._cost_residual_matrix = (
            self._get_residual_matrices()
        )
        self._minimize_cost()
        self._min_cost = self._get_cost_by_flow()

    @property
    def min_cost(self) -> int:
        """Возвращает минимальную стоимость потока"""
        return self._min_cost

    def _minimize_cost(self) -> None:
        """Осуществляет минимизацию стоимости максимального потока
        посредством поиска и удаления отрицательных циклов в остаточной сети.
        После удаления всех циклов обновляет матрицу локальных потоков
        на основе остаточной сети."""
        
        while True:
            loop = None
            for start_idx in range(self._order):
                loop = self._find_negative_loop(start_idx)
                if loop and len(loop) > 1:
                    break
            
            if not loop or len(loop) <= 1:
                break
            
            self._remove_negative_loop(loop)

    def _find_negative_loop(self, start_vertex_idx) -> list[int]:
        """Возвращает найденный цикл отрицательной стоимости в остаточной сети
        стоимости транспортировки"""
        
        order = self._order
        distances = [inf] * order
        distances[start_vertex_idx] = 0
        predecessors = [None] * order
        
        edges = []
        for i in range(order):
            for j in range(order):
                if self._cost_residual_matrix[i][j]:
                    edges.append((i, j))
        
        last_updated = None
        for iteration in range(order):
            last_updated = None
            for src, trg in edges:
                if distances[src] != inf:
                    new_dist = distances[src] + self._cost_residual_matrix[src][trg]
                    if new_dist < distances[trg]:
                        distances[trg] = new_dist
                        predecessors[trg] = src
                        last_updated = trg
            
            if iteration == order - 1 and last_updated is not None:
                return self._restore_loop(predecessors, last_updated)
        
        return []

    def _restore_loop(self, predecessors: list[int], vertex_idx: int) -> list[int]:
        """Восстанавливает цикл из информации о предшественниках"""
        visited = {}
        current = vertex_idx
        position = 0
        
        while current is not None:
            if current in visited:
                cycle_start_pos = visited[current]
                cycle = []
                temp = current
                temp_path = []
                while True:
                    temp_path.append(temp)
                    temp = predecessors[temp]
                    if temp == current:
                        break
                temp_path.append(current)
                return temp_path[::-1]
            
            visited[current] = position
            position += 1
            current = predecessors[current]
        
        return []

    def _remove_negative_loop(self, loop) -> None:
        """Удаляет цикл отрицательной стоимости в остаточных сетях потоков и стоимостей."""
        
        if not loop or len(loop) < 2:
            return
        
        min_capacity = inf
        for i in range(len(loop) - 1):
            from_idx = loop[i]
            to_idx = loop[i + 1]
            capacity = self._residual_matrix[from_idx][to_idx]
            if capacity > 0:
                min_capacity = min(min_capacity, capacity)
        
        if min_capacity <= 0 or min_capacity == inf:
            return
        
        for i in range(len(loop) - 1):
            from_idx = loop[i]
            to_idx = loop[i + 1]
            
            cost = self._cost_residual_matrix[from_idx][to_idx]
            
            if cost < 0:
                self._flow_matrix[from_idx][to_idx] -= min_capacity
            else:
                self._flow_matrix[to_idx][from_idx] += min_capacity
        
        self._residual_matrix, self._cost_residual_matrix = self._get_residual_matrices()

    def _get_residual_matrices(self):
        """Возвращает остаточные сети, созданные на основе матриц
        локальных потоков и пропускных способностей:
        - residual_matrix - остаточная сеть с указанием потоков и резервов.
        - cost_residual_matrix - остаточная сеть с указанием стоимости транспортировки.
        """
        residual_matrix = [[0] * self._order for _ in range(self._order)]
        cost_residual_matrix = [[0] * self._order for _ in range(self._order)]
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                flow = self._flow_matrix[row_idx][col_idx]
                reserve = (
                    self._capacity_matrix[row_idx][col_idx]
                    - self._flow_matrix[row_idx][col_idx]
                )
                cost = self._cost_matrix[row_idx][col_idx]
                if flow:
                    residual_matrix[row_idx][col_idx] = flow
                    cost_residual_matrix[row_idx][col_idx] = -cost
                if reserve:
                    residual_matrix[col_idx][row_idx] = reserve
                    cost_residual_matrix[col_idx][row_idx] = cost

        return residual_matrix, cost_residual_matrix

    def _get_cost_by_flow(self) -> int:
        """Возвращает суммарную стоимость транспортировки на основе матрицы локальных потоков
        и матрицы стоимостей"""
        
        total_cost = 0
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if self._flow_matrix[row_idx][col_idx]:
                    total_cost += self._flow_matrix[row_idx][col_idx] * self._cost_matrix[row_idx][col_idx]
        
        return total_cost


if __name__ == "__main__":
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0],  # c
        [0, 0, 0, 0, 0, 13],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    cost_matrix = [
        # s a  b  c  d  t
        [0, 3, 2, 4, 0, 0],  # s
        [0, 0, 0, 4, 5, 0],  # a
        [0, 2, 0, 2, 0, 0],  # b
        [0, 0, 0, 0, 2, 0],  # c
        [0, 0, 0, 0, 0, 1],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример решения задачи поиска максимального потока минимальной стоимости:")
    calculator = MinCostFlowCalculator(capacity_matrix, cost_matrix)
    print("Величина максимального потока:", calculator._max_flow)
    print("Стоимость потока:", calculator._min_cost)
    print("Матрица локальных потоков")
    for row in calculator._flow_matrix:
        print(row)