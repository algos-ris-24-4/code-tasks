from math import inf

from network_flow.max_flow_calculator import MaxFlowCalculator
from network_flow.network_validator import NetworkValidator

COST_MATRIX_NAME = "Таблица стоимости транспортировки"


class MinCostFlowCalculator(MaxFlowCalculator):
    """Класс для решения задачи поиска максимального потока минимальной стоимости"""

    def __init__(self, capacity_matrix: list[list[int]], cost_matrix: list[list[int]]):
        """
        Конструктор класса.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        :param cost_matrix: Квадратная матрица стоимости транспортировки (неотрицательные целые).
        :type cost_matrix: list[list[int]]
        """
        NetworkValidator.validate_matrix(capacity_matrix, "Таблица пропускных способностей")
        NetworkValidator.validate_matrix(cost_matrix, COST_MATRIX_NAME)

        vertices = MaxFlowCalculator.split_vertices_by_types(capacity_matrix)
        NetworkValidator.validate_vertices(vertices, "Таблица пропускных способностей")

        self._capacity_matrix = capacity_matrix
        self._cost_matrix = cost_matrix
        self._order = len(capacity_matrix)
        self._source_idx = vertices.sources[0]
        self._sink_idx = vertices.sinks[0]

        self._flow_matrix: list[list[int]] = [
            [0] * self._order for i in range(self._order)
        ]
        self._max_flow: int = 0
        self._min_cost: int = 0

        self._calculate_min_cost_max_flow()

    @property
    def min_cost(self) -> int:
        """Возвращает минимальную стоимость потока"""
        return self._min_cost

    def _calculate_min_cost_max_flow(self) -> None:
        """Вычисляет максимальный поток минимальной стоимости с помощью поиска кратчайших увеличивающих путей."""
        order = self._order
        src = self._source_idx
        trg = self._sink_idx

        residual_capacity = [[0] * order for i in range(order)]
        residual_cost = [[0] * order for i in range(order)]

        for i in range(order):
            for j in range(order):
                capacity = self._capacity_matrix[i][j]
                if capacity:
                    cost = self._cost_matrix[i][j]
                    residual_capacity[i][j] = capacity
                    residual_cost[i][j] = cost
                    residual_cost[j][i] = -cost

        while True:
            dist = [inf] * order
            parent = [-1] * order
            dist[src] = 0

            for i in range(order - 1):
                updated = False
                for u in range(order):
                    if dist[u] == inf:
                        continue
                    for v in range(order):
                        if residual_capacity[u][v] <= 0:
                            continue
                        new_dist = dist[u] + residual_cost[u][v]
                        if new_dist < dist[v]:
                            dist[v] = new_dist
                            parent[v] = u
                            updated = True
                if not updated:
                    break

            if dist[trg] == inf:
                break

            path = []
            v = trg
            while v != -1 and v != src:
                path.append(v)
                v = parent[v]
            if v == -1:
                break
            path.append(src)
            path = path[::-1]

            delta = inf
            for i in range(1, len(path)):
                u = path[i - 1]
                v = path[i]
                delta = min(delta, residual_capacity[u][v])

            if delta == inf or delta == 0:
                break

            for i in range(1, len(path)):
                u = path[i - 1]
                v = path[i]
                residual_capacity[u][v] -= delta
                residual_capacity[v][u] += delta

                if self._capacity_matrix[u][v]:
                    self._flow_matrix[u][v] += delta
                elif self._capacity_matrix[v][u]:
                    self._flow_matrix[v][u] -= delta

            self._max_flow += delta

        total_cost = 0
        for i in range(order):
            for j in range(order):
                flow = self._flow_matrix[i][j]
                if flow:
                    total_cost += flow * self._cost_matrix[i][j]
        self._min_cost = total_cost

    def _get_residual_matrices(self):
        raise NotImplementedError

    def _get_cost_by_flow(self) -> int:
        return self._min_cost


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
