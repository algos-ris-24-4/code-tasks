from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching


def hungarian(matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Реализация венгерского алгоритма для решения задачи о назначениях.

    :param matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type matrix: list[list[int|float]]
    :return: Матрица смежности, где ``True`` означает включение ребра в паросочетание.
    :rtype: list[list[bool]]
    """
    order = len(matrix)
    matching = BipartiteGraphMatching(order)
    reduced_matrix = get_reduced_matrix(matrix)

    while not matching.is_perfect:
        bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
        X, Y = set(), set()
        parent = {}
        free_left = next((i for i in range(order) if not matching.is_left_covered(i)), None)
        if free_left is None:
            break
        wave = deque([(True, free_left)])
        X.add(free_left)
        visited_left, visited_right = {free_left}, set()
        path = None

        while wave:
            is_left, idx = wave.popleft()
            if is_left:
                for j in bipartite_graph.right_neighbors(idx):
                    if j not in visited_right:
                        visited_right.add(j)
                        Y.add(j)
                        parent[(False, j)] = (True, idx)
                        if not matching.is_right_covered(j):
                            path = []
                            cur = (False, j)
                            while cur in parent:
                                prev = parent[cur]
                                path.append((prev[1], cur[1]) if prev[0] else (cur[1], prev[1]))
                                cur = prev
                            path.reverse()
                            break
                        left_match = matching.get_left_match(j)
                        if left_match not in visited_left:
                            visited_left.add(left_match)
                            X.add(left_match)
                            parent[(True, left_match)] = (False, j)
                            wave.append((True, left_match))
                if path is not None:
                    break

        if path:
            for left, right in path:
                if matching.is_left_covered(left):
                    matching.remove_edge(left, matching.get_right_match(left))
                if matching.is_right_covered(right):
                    matching.remove_edge(matching.get_left_match(right), right)
                matching.add_edge(left, right)
        else:
            delta = min(
                reduced_matrix[i][j]
                for i in X for j in range(order) if j not in Y
            ) if X else float("inf")
            if delta > 0 and delta != float("inf"):
                for i in X:
                    for j in range(order):
                        reduced_matrix[i][j] -= delta
                for j in Y:
                    for i in range(order):
                        reduced_matrix[i][j] += delta

    return matching


def _get_bipartite_graph_by_zeros(reduced_matrix: list[list[int | float]]) -> BipartiteGraph:
    adjacency_lists = {}
    for row_idx in range(len(reduced_matrix)):
        adjacency_lists[row_idx] = [col_idx for col_idx, value in enumerate(reduced_matrix[row_idx]) if value == 0]
    return BipartiteGraph(adjacency_lists)


def get_reduced_matrix(matrix: list[list[int | float]]) -> list[list[int | float]]:
    """
    Выполняет редукцию матрицы, уменьшая значения в строках и столбцах.

    :param matrix: Исходная квадратная матрица весов.
    :type matrix: list[list[int|float]]
    :return: Редуцированная матрица, где минимальные значения в строках и столбцах равны 0.
    :rtype: list[list[int|float]]
    """
    reduced_matrix = [[val - min(row) for val in row] for row in matrix]

    for col_idx in range(len(reduced_matrix[0])):
        min_col_value = reduced_matrix[0][col_idx]
        for row_idx in range(1, len(reduced_matrix)):
            if reduced_matrix[row_idx][col_idx] < min_col_value:
                min_col_value = reduced_matrix[row_idx][col_idx]
        for row_idx in range(len(reduced_matrix)):
            reduced_matrix[row_idx][col_idx] -= min_col_value

    return reduced_matrix

if __name__ == "__main__":
    matrix = [
        [6, 7, 8, 14, 7],
        [8, 14, 6, 9, 7],
        [14, 14, 13, 9, 11],
        [5, 12, 10, 9, 14],
        [6, 10, 8, 10, 15],
    ]
    print("Исходная матрица")
    for row in matrix:
        print(row)
    print()

    reduced_matrix = get_reduced_matrix(matrix)
    print("Редуцированная матрица")
    for row in reduced_matrix:
        print(row)
    print()

    bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
    print("Двудольный граф")
    print(bipartite_graph)
    print()

    matching = hungarian(matrix)
    print("Совершенное паросочетание найденное венгерским алгоритмом")
    print(matching.get_matching())