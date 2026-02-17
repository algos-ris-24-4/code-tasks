from collections import deque
from math import inf
from network_flow.data_types import NetworkVerticesData
from network_flow.network_validator import NetworkValidator

CAPACITY_MATRIX_NAME = "Таблица пропускных способностей"


class MaxFlowCalculator:
    """Класс для решения задачи поиска максимального потока в сети"""

    def __init__(self, capacity_matrix: list[list[int]]):
        """
        Конструктор класса.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        """

        NetworkValidator.validate_matrix(capacity_matrix, CAPACITY_MATRIX_NAME)
        vertices = MaxFlowCalculator.split_vertices_by_types(capacity_matrix)
        NetworkValidator.validate_vertices(vertices, CAPACITY_MATRIX_NAME)

        self._capacity_matrix = capacity_matrix
        self._order = len(capacity_matrix)
        self._source_idx = vertices.sources[0]
        self._sink_idx = vertices.sinks[0]
        
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if capacity_matrix[row_idx][col_idx]:
                    self._residual_matrix[col_idx][row_idx] = self._capacity_matrix[row_idx][col_idx]

        self._max_flow = None
        self._flow_matrix = None
        self._calculate_max_flow()

    @property
    def max_flow(self) -> int:
        """Возвращает максимальное значение потока"""
        return self._max_flow

    @property
    def flow_matrix(self) -> tuple[tuple[int]]:
        """Возвращает матрицу локальных потоков"""
        return tuple([tuple(row) for row in self._flow_matrix])

    @staticmethod
    def split_vertices_by_types(matrix) -> NetworkVerticesData:
        """
        Разделяет вершины сети на три категории: источники, стоки и транзитные вершины.
        :param matrix: Квадратная матрица пропускных способностей графа.
        :type matrix: list[list[int]]
        :return: Данные о вершинах сети, содержащие источники, стоки и транзиты.
        :rtype: NetworkVerticesData
        """
        n = len(matrix)
        row_sum = [sum(row) for row in matrix]
        col_sum = [sum(matrix[i][j] for i in range(n)) for j in range(n)]  

        sources = []
        sinks = []
        transits = []

        for i in range(n):
            has_outgoing = row_sum[i] > 0
            has_incoming = col_sum[i] > 0

            if not has_incoming:
                sources.append(i) 
            elif not has_outgoing and has_incoming:
                sinks.append(i)  
            else:
                transits.append(i)                     

        return NetworkVerticesData(sources, sinks, transits)

    def _calculate_max_flow(self) -> None:
        """Вычисляет максимальный поток алгоритмом Форда-Фалкерсона"""
        self._flow_matrix = [[0] * self._order for _ in range(self._order)]
        self._max_flow = 0        
        
        while True:
            path = self._find_augmenting_path()
            if not path:
                break

            path_flow = inf
            for i in range(len(path) - 1):
                first_vertex = path[i]
                second_vertex = path[i + 1]
                cap = self._residual_matrix[second_vertex][first_vertex]
                if cap < path_flow:
                    path_flow = cap

            self._increase_flow(path, path_flow)
            self._max_flow += path_flow

        self._set_flow_matrix_by_residual_matrix()

    def _set_flow_matrix_by_residual_matrix(self):
        """Заполняет матрицу потоков на основе остаточной сети"""
        for i in range(self._order):
            for j in range(self._order):
                if self._capacity_matrix[i][j] > 0:
                    self._flow_matrix[i][j] = self._residual_matrix[i][j]

    def _find_augmenting_path(self):
        """
        Возвращает увеличивающий путь в виде списка вершин от истока к стоку.
        """
        visited = [False] * self._order
        parent = [-1] * self._order
        queue = deque([self._sink_idx])
        visited[self._sink_idx] = True

        while queue:
            start_vertex = queue.popleft()
            for vertex in range(self._order):
                if not visited[vertex] and self._residual_matrix[start_vertex][vertex] > 0:
                    visited[vertex] = True
                    parent[vertex] = start_vertex
                    if vertex == self._source_idx:
                        path = []
                        cur = vertex
                        while cur != -1:
                            path.append(cur)
                            cur = parent[cur]
                        return path 
                    queue.append(vertex)
        return None

    def _increase_flow(self, path, path_flow: int):
        """
        Корректирует остаточную сеть: уменьшает пропускную способность обратных рёбер
        и увеличивает прямые.
        """
        for i in range(len(path) - 1):
            first_vertex = path[i]
            second_vertex = path[i + 1]
            self._residual_matrix[second_vertex][first_vertex] -= path_flow
            self._residual_matrix[first_vertex][second_vertex] += path_flow


if __name__ == "__main__":
    vertex_names = ["s", "a", "b", "c", "d", "t"]
    capacity_matrix = [
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0], # c
        [0, 0, 0, 0, 0, 13], # d
        [0, 0, 0, 0, 0, 13], # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример решения задачи поиска максимального потока в сети:")
    max_flow_data = MaxFlowCalculator(capacity_matrix)
    print("Величина максимального потока:", max_flow_data.max_flow)
    print("Матрица локальных потоков")
    for row in max_flow_data.flow_matrix:
        print(row)