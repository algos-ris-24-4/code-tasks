from matching.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from collections import deque

from matching.errors.perfect_matching_error import PerfectMatchingError

#Поиск совершенного паросочетания
def get_perfect_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)

    order = bipartite_graph.order
    matching = BipartiteGraphMatching(order)

    while not matching.is_perfect:
        start_left = find_uncovered_left(order, matching) # Находит непокрытую вершину
        end_right, previous = bfs_wave(start_left, bipartite_graph, matching) # Ищет путь (Цепь) для инвертирования

        if end_right is None:
            raise PerfectMatchingError(
                ErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH
            )

        augment_along_path(end_right, previous, matching) # Инвертация вершин для нахождения совершенного паросочетания

    return matching


def find_uncovered_left(order: int, matching: BipartiteGraphMatching) -> int:
    for left in range(order):
        if not matching.is_left_covered(left):
            return left
    return -1


def bfs_wave(start_left: int, graph: BipartiteGraph, matching: BipartiteGraphMatching):

    queue = deque()
    queue.append(('L', start_left)) # Очередь для итерации 

    previous = {}  # Словарь для восстановления пути 
     
    visited_left = {start_left}
    visited_right = set()

    while queue:
        side, vertex = queue.popleft()

        if side == 'L': # Работа с левой частью
            for right in graph.right_neighbors(vertex):
                if right in visited_right: # посещали ли раньше?
                    continue
                if matching.is_left_covered(vertex) and matching.get_right_match(vertex) == right: # Проверка на покрытие
                    continue

                visited_right.add(right) 
                previous[('R', right)] = ('L', vertex)

                if not matching.is_right_covered(right): # Если правая вершина не покрыта, то мы нашли путь.
                    return right, previous

                queue.append(('R', right)) # Если путь на данной вершине не закончен, то мы добавляем его в очередь

        else: # Работа с правой частью
            left = matching.get_left_match(vertex)
            if left not in visited_left: # Проверка на посещение 
                visited_left.add(left) 
                previous[('L', left)] = ('R', vertex)
                queue.append(('L', left)) # Добавляем в очередь

    return None, None


def augment_along_path(end_right: int, previous: dict, matching: BipartiteGraphMatching):
    current = ('R', end_right)

    while current in previous:
        prev = previous[current]

        if current[0] == 'R' and prev[0] == 'L':
            left, right = prev[1], current[1]
            if matching.is_left_covered(left):
                old_right = matching.get_right_match(left)
                matching.remove_edge(left, old_right)
            matching.add_edge(left, right)

        current = previous.get(prev)


if __name__ == "__main__":
    print("Исходный двудольный граф")
    bipartite_graph = BipartiteGraph({
        0: [0, 1],
        1: [0, 4],
        2: [1, 2, 3],
        3: [1, 2, 4],
        4: [0, 4],
    })
    print(bipartite_graph)

    print("Полученное паросочетание")
    print(get_perfect_matching(bipartite_graph))
