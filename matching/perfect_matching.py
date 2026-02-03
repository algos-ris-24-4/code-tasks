from matching.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from collections import deque

from matching.errors.perfect_matching_error import PerfectMatchingError


def get_perfect_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит совершенное паросочетание в двудольном графе с долями равной мощности.

    Алгоритм последовательно ищет увеличивающие (чередующиеся) пути относительно текущего
    паросочетания, начиная с пустого. Каждый найденный путь используется для увеличения
    мощности паросочетания на единицу. Процесс продолжается, пока существуют непокрытые
    вершины в левой доле и найдены увеличивающие пути.

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :return: Объект BipartiteGraphMatching, представляющий совершенное паросочетание.
    :raises PerfectMatchingError: Если совершенное паросочетание не существует в данном графе.
    """
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)
    
    matching = BipartiteGraphMatching(bipartite_graph.order)

    uncovered_left = get_uncovered_left_part(matching, bipartite_graph)
    while True:
        chain = get_alternating_chain()
        if chain:
            increase_matching(chain, matching)
            uncovered_left = get_uncovered_left_part(matching, bipartite_graph)
        else:
            break

    if not matching.is_perfect:
        raise ErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH

    return matching


def get_uncovered_left_part(matching: BipartiteGraphMatching, graph: BipartiteGraph) -> list[int]:
    return [vertex for vertex in range(graph.order) if matching.is_left_covered(vertex)]


def get_alternating_chain(matching: BipartiteGraphMatching, uncovered_left_part: list[int]) -> list[int]:
    chain = []

    ...

    return chain


def increase_matching(altng_chain: list[int], matching: BipartiteGraphMatching):
    for vertex_idx in range(1, len(altng_chain) - 1, 2):
        edge_start, edge_end = altng_chain[vertex_idx], altng_chain[vertex_idx + 1]
        matching.remove_edge(edge_start, edge_end)
    
    for vertex_idx in range(len(altng_chain) - 1, 2):
        edge_start, edge_end = altng_chain[vertex_idx], altng_chain[vertex_idx + 1]
        matching.add_edge(edge_start, edge_end)
    
        


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
