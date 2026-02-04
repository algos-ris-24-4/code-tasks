import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

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
    if order == 0:
        return BipartiteGraphMatching(0)
    matching = BipartiteGraphMatching(order)
    reduced_matrix = get_reduced_matrix(matrix)

    while not matching.is_perfect:
        bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
        found_augmenting_path = False

        for root in range(order):
            if matching.is_left_covered(root):
                continue

            # Начало построения чередующегося дерева
            attended_left = [False] * order
            attended_right = [False] * order
            work_parents = [-1] * order

            attended_left[root] = True

            # Создаем 2 очереди: одна для четных фронтов, а вторая для нечетных
            even_queue = deque([root])
            odd_queue = deque()

            augment_target: Optional[int] = None

            while (even_queue or odd_queue) and augment_target is None:
                while even_queue and augment_target is None:
                    tasks = even_queue.popleft()
                    for workers in bipartite_graph.right_neighbors(tasks):
                        if attended_right[workers]:
                            continue
                        attended_right[workers] = True
                        work_parents[workers] = tasks
                        odd_queue.append(workers)
                        if not matching.is_right_covered(workers):
                            augment_target = workers
                            break

                while odd_queue and augment_target is None:
                    workers = odd_queue.popleft()
                    matched_task = matching.get_left_match(workers)
                    if matched_task != -1 and not attended_left[matched_task]:
                        attended_left[matched_task] = True
                        even_queue.append(matched_task)

            if augment_target is not None:
                workers = augment_target
                while workers != -1:
                    tasks = work_parents[workers]
                    old_workers = matching.get_right_match(tasks)
                    if old_workers != -1:
                        matching.remove_edge(tasks, old_workers)
                    if workers != -1:
                        matching.add_edge(tasks, workers)
                    workers = old_workers
                found_augmenting_path = True
                break


        if found_augmenting_path:
            continue

        # Начало диагональной редукции
        tree_tasks: Set[int] = {i for i in range(order) if attended_left[i]}
        tree_workers: Set[int] = {j for j in range(order) if attended_right[j]}

        if not tree_tasks:
            raise RuntimeError("Не удалось построить чередующееся дерево")

        min_element = min(
            reduced_matrix[i][j]
            for i in tree_tasks
            for j in range(order)
            if j not in tree_workers
        )

        if min_element <= 0:
            raise RuntimeError(f"Некорректное значение min_element: {min_element}")

        for i in tree_tasks:
            for j in range(order):
                reduced_matrix[i][j] -= min_element
        for j in tree_workers:
            for i in range(order):
                reduced_matrix[i][j] += min_element

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