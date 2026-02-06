from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching


def hungarian(matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Реализация венгерского алгоритма для решения задачи о назначениях.

    :param matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type matrix: list[list[int|float]]
    :return: Совершенное паросочетание с минимальной стоимостью.
    :rtype: BipartiteGraphMatching
    """
    order = len(matrix)
    matching = BipartiteGraphMatching(order)
    reduced_matrix = get_reduced_matrix(matrix)
    bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)

    while not matching.is_perfect:
        graph = _get_bipartite_graph_by_zeros(reduced_matrix)

        start_vertex = -1
        for i in range(order):
            if not matching.is_left_covered(i):
                start_vertex = i
                break
        
        if start_vertex == -1:
            break

        found_path, path_end_vertex, marked_left, marked_right, parent_left, parent_right = \
            _build_alternating_tree(matching, graph, start_vertex, order)
        
        if found_path:
            _augment_matching(matching, start_vertex, path_end_vertex, parent_left, parent_right)
            continue 

        has_unmarked_left = any(marked_left[i] == 0 for i in range(order))
        has_unmarked_right = any(marked_right[j] == 0 for j in range(order))
        
        if not has_unmarked_left or not has_unmarked_right:
            raise ValueError("Невозможно выполнить диагональную редукцию")

        _diagonal_reduction(reduced_matrix, marked_left, marked_right, order)

    return matching


def _build_alternating_tree(matching: BipartiteGraphMatching,
                          graph: BipartiteGraph,
                          start_vertex: int,
                          order: int) -> tuple[bool, int, list[int], list[int], list[int], list[int]]:
    """
    Строит чередующееся дерево из заданной вершины.
    
    :param matching: Текущее паросочетание
    :param graph: Двудольный граф
    :param start_vertex: Стартовая левая вершина
    :param order: Порядок графа
    :return: (found_path, path_end_vertex, marked_left, marked_right, parent_left, parent_right)
    """

    marked_left = [0] * order
    marked_right = [0] * order
    parent_right = [-1] * order
    parent_left = [-1] * order   
    
    queue = deque()
    queue.append(start_vertex)
    marked_left[start_vertex] = 1
    
    path_end = -1
    
    while queue:
        current_left = queue.popleft()
        
        for right_neighbor in graph.right_neighbors(current_left):
            if marked_right[right_neighbor] == 0:
                marked_right[right_neighbor] = 1
                parent_right[right_neighbor] = current_left
                
                if not matching.is_right_covered(right_neighbor):
                    path_end = right_neighbor
                    return True, path_end, marked_left, marked_right, parent_left, parent_right
                
                matched_left = matching.get_left_match(right_neighbor)
                if matched_left != -1 and marked_left[matched_left] == 0:
                    marked_left[matched_left] = 1
                    parent_left[matched_left] = right_neighbor
                    queue.append(matched_left)

    return False, -1, marked_left, marked_right, parent_left, parent_right


def _augment_matching(matching: BipartiteGraphMatching,
                     start_vertex: int,
                     path_end_vertex: int,
                     parent_left: list[int],
                     parent_right: list[int]) -> None:
    """
    Увеличивает паросочетание по найденной увеличивающей цепи.
    
    :param matching: Текущее паросочетание
    :param start_vertex: Начальная вершина цепи (корень дерева)
    :param path_end_vertex: Конечная вершина цепи (свободная правая вершина)
    :param parent_left: Массив родителей для левых вершин
    :param parent_right: Массив родителей для правых вершин
    """

    chain = []
    current_vertex = path_end_vertex
    
    while True:
        chain.append(current_vertex) 
        prev_left = parent_right[current_vertex]
        chain.append(prev_left )
        
        if prev_left == start_vertex:
            break
            
        current_vertex = parent_left[prev_left]
    
    chain.reverse()
    
    for i in range(0, len(chain), 2):
        left_vertex = chain[i]
        right_vertex = chain[i + 1]
        
        if matching.is_left_covered(left_vertex):
            old_right_match = matching.get_right_match(left_vertex)
            matching.remove_edge(left_vertex, old_right_match)
        
        if matching.is_right_covered(right_vertex):
            old_left_match = matching.get_left_match(right_vertex)
            matching.remove_edge(old_left_match, right_vertex)

        matching.add_edge(left_vertex, right_vertex)


def _diagonal_reduction(matrix: list[list[int | float]], 
                       marked_left: list[int], 
                       marked_right: list[int], 
                       order: int) -> None:
    """
    Выполняет диагональную редукцию матрицы.
    
    :param matrix: Матрица для редукции
    :param marked_left: Массив пометок левых вершин (0 = не помечена, 1 = помечена)
    :param marked_right: Массив пометок правых вершин (0 = не помечена, 1 = помечена)
    :param order: Порядок матрицы
    :raises PerfectMatchingError: Если не удалось найти подходящий δ
    """
    
    min_value = float('inf')
    for i in range(order):
        if marked_left[i] == 1:
            for j in range(order):
                if marked_right[j] == 0: 
                    if matrix[i][j] < min_value:
                        min_value = matrix[i][j]

    for i in range(order):
        if marked_left[i] == 1:
            for j in range(order):
                matrix[i][j] -= min_value
    
    for j in range(order):
        if marked_right[j] == 1:
            for i in range(order):
                matrix[i][j] += min_value

    for i in range(order):
            has_zero = any(matrix[i][j] == 0 for j in range(order))
            if not has_zero:
                matrix = get_reduced_matrix(matrix)
                
    return matrix

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
