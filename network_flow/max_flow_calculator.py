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

        self._residual_matrix = [[0] * self._order for _ in range(self._order)]
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if capacity_matrix[row_idx][col_idx]:
                    self._residual_matrix[col_idx][row_idx] = self._capacity_matrix[row_idx][col_idx]

        self._max_flow: int = None
        self._flow_matrix = None
        # Процедура _calculate_max_flow должна в ходе выполнения заполнить атрибуты _flow_matrix и _max_flow
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
        sources = []
        for col_idx in range(len(matrix)):
            capacity_sum = 0
            for row_idx in range(len(matrix)):
                capacity_sum += matrix[row_idx][col_idx]

            if capacity_sum == 0:
                sources.append(col_idx)

        sinks_set = set()
        for row_idx in range(len(matrix)):
            capacity_sum = 0
            for col_idx in range(len(matrix)):
                capacity_sum += matrix[row_idx][col_idx]

            if capacity_sum == 0:
                sinks_set.add(row_idx)
        sinks = list(sinks_set)

        transits = []
        for col_idx in range(len(matrix)):
            capacity_sum = 0
            for row_idx in range(len(matrix)):
                capacity_sum += matrix[row_idx][col_idx]

            if capacity_sum != 0 and col_idx not in sinks_set:
                transits.append(col_idx)

        return NetworkVerticesData(sources, sinks, transits)


    def _calculate_max_flow(self) -> None: 
        """Вычисляет максимальный поток в сети с использованием алгоритма Форда-Фалкерсона"""
        while True:
            augmenting_path = self._find_augmenting_path()
            if len(augmenting_path) == 0:
                return
            self._increase_flow(augmenting_path)
            self._set_flow_matrix_by_residual_matrix()


    def _set_flow_matrix_by_residual_matrix(self) -> None:
        """Обновляет матрицу локальных потоков на основе остаточной сети"""
        self._flow_matrix = [[0]* self._order for _ in range(self._order)]
        for from_vrtx in range(self._order):
            for to_vrtx in range(self._order):
                if self._capacity_matrix[from_vrtx][to_vrtx] > 0:
                    self._flow_matrix[from_vrtx][to_vrtx] = self._residual_matrix[from_vrtx][to_vrtx]

        result_flow = 0
        for to_vrtx in range(self._order):
            result_flow += self._flow_matrix[self._source_idx][to_vrtx]

        self._max_flow = result_flow
        

    def _find_augmenting_path(self) -> list[int]:
        """Возвращает найденный увеличивающий путь в сети"""
        src = self._sink_idx
        trg = self._source_idx
        deq = deque()
        visited = set()
        parents = [-1] * self._order

        deq.append(src)
        visited.add(src)

        while deq:
            vertex = deq.popleft()
            for adj_idx, edge_capacity in enumerate(self._residual_matrix[vertex]):
                if edge_capacity > 0 and adj_idx not in visited:
                    visited.add(adj_idx)
                    deq.append(adj_idx)
                    parents[adj_idx] = vertex

                    if adj_idx == trg:
                        return MaxFlowCalculator._recover_path(parents, src, trg)
        return []


    @staticmethod            
    def _recover_path(parents: list[int], end: int) -> list[int]:
        """Возвращает восстановленный путь между двумя вершинами"""
        path = []
        vrtx = end
        while vrtx != -1:
            path.append(vrtx)
            vrtx = parents[vrtx]
        return path


    def _increase_flow(self, augmenting_path: list[int]) -> None:
        """Корректирует остаточную сеть для увеличения потока в сети с использованием
        найденного увеличивающего пути"""
        min_capacity = float("inf")
        for vrtx in range(len(augmenting_path) - 1):
            current_vrtx = augmenting_path[vrtx]
            next_vrtx = augmenting_path[vrtx + 1]

            current_capacity = self._residual_matrix[next_vrtx][current_vrtx]
            min_capacity = min(min_capacity,current_capacity)

        for vrtx in range(len(augmenting_path) - 1):
            current_vrtx = augmenting_path[vrtx]
            next_vrtx = augmenting_path[vrtx + 1]

            self._residual_matrix[next_vrtx][current_vrtx] -= min_capacity 
            self._residual_matrix[current_vrtx][next_vrtx] += min_capacity 



if __name__ == "__main__":
    vertex_names = ["s", "a", "b", "c", "d", "t"]
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0],  # c
        [0, 0, 0, 0, 0, 13],  # d
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
