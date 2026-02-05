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

        left_tree: set[int] = set()
        right_tree: set[int] = set()
        parent: dict[tuple[bool, int], tuple[bool, int]] = {}

        free_left = next((i for i in range(order) if not matching.is_left_covered(i)), None)
        if free_left is None:
            break

        queue = deque([(True, free_left)])
        left_tree.add(free_left)
        visited_left, visited_right = {free_left}, set()
        augmenting_path: list[tuple[int, int]] | None = None

        while queue and augmenting_path is None:
            is_left, idx = queue.popleft()
            if not is_left:
                continue

            for right_idx in bipartite_graph.right_neighbors(idx):
                if right_idx in visited_right:
                    continue
                visited_right.add(right_idx)
                right_tree.add(right_idx)
                parent[(False, right_idx)] = (True, idx)

                if not matching.is_right_covered(right_idx):
                    path: list[tuple[int, int]] = []
                    cur = (False, right_idx)
                    while cur in parent:
                        prev = parent[cur]
                        path.append((prev[1], cur[1]) if prev[0] else (cur[1], prev[1]))
                        cur = prev
                    path.reverse()
                    augmenting_path = path
                    break

                matched_left = matching.get_left_match(right_idx)
                if matched_left not in visited_left:
                    visited_left.add(matched_left)
                    left_tree.add(matched_left)
                    parent[(True, matched_left)] = (False, right_idx)
                    queue.append((True, matched_left))

        if augmenting_path:
            for left_idx, right_idx in augmenting_path:
                if matching.is_left_covered(left_idx):
                    matching.remove_edge(left_idx, matching.get_right_match(left_idx))
                if matching.is_right_covered(right_idx):
                    matching.remove_edge(matching.get_left_match(right_idx), right_idx)
                matching.add_edge(left_idx, right_idx)
        else:
            candidates = [
                reduced_matrix[i][j]
                for i in left_tree
                for j in range(order)
                if j not in right_tree
            ]
            delta = min(candidates) if candidates else float("inf")

            if delta > 0 and delta != float("inf"):
                for i in left_tree:
                    for j in range(order):
                        reduced_matrix[i][j] -= delta
                for j in right_tree:
                    for i in range(order):
                        reduced_matrix[i][j] += delta
            else:
                break

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