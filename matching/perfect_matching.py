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
        chain = get_alternating_chain(matching,bipartite_graph,uncovered_left)
        if chain:
            increase_matching(chain, matching)
            uncovered_left = get_uncovered_left_part(matching, bipartite_graph)
        else:
            break

    if not matching.is_perfect:
        raise PerfectMatchingError(ErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH)

    return matching


def get_uncovered_left_part(matching: BipartiteGraphMatching, graph: BipartiteGraph) -> list[int]:
    return [vertex for vertex in range(graph.order) if not matching.is_left_covered(vertex)]


def get_alternating_chain(matching: BipartiteGraphMatching, graph: BipartiteGraph, uncovered_left_part: list[int]) -> list[int]:
    chain = []
    if len(uncovered_left_part) == 0:
        return None

    visited_left_vertexes = set()
    visited_right_vertexes = set()

    parent_left_vertex = {}
    parent_right_vertex = {}

    uncovered_right_vertex = None

    deq = deque()
    for vrtx in uncovered_left_part:
        deq.append(('Left',vrtx))
        visited_left_vertexes.add(vrtx)
    
    while deq and uncovered_right_vertex == None:
        side, vrtx = deq.popleft()
        if side == "Left":
           left_vrtx = vrtx
           for right_vrtx in graph.right_neighbors(left_vrtx):
               if right_vrtx in visited_right_vertexes:
                   continue
               elif matching.get_right_match(left_vrtx) == right_vrtx:
                   continue
               
               visited_right_vertexes.add(right_vrtx)
               parent_right_vertex[right_vrtx] = left_vrtx
               
               if not matching.is_right_covered(right_vrtx):
                    uncovered_right_vertex = right_vrtx
                    break
               
               deq.append(('Right',right_vrtx))

        else: 
            right_vrtx = vrtx
            covered_left_vrtx = matching.get_left_match(right_vrtx)

            if covered_left_vrtx == -1:
                continue

            if covered_left_vrtx not in visited_left_vertexes:
                visited_left_vertexes.add(covered_left_vrtx)
                parent_left_vertex[covered_left_vrtx] = right_vrtx
                
                deq.append(('Left',covered_left_vrtx))
    
    if uncovered_right_vertex is None:
        return None 
    
    right_vrtx = uncovered_right_vertex
    chain.append(right_vrtx)

    while True:
        left_vrtx = parent_right_vertex[right_vrtx]
        chain.append(left_vrtx)

        if left_vrtx not in parent_left_vertex:
            break
        else:
            right_vrtx = parent_left_vertex[left_vrtx]
            chain.append(right_vrtx)
    chain.reverse()

    return chain


def increase_matching(altng_chain: list[int], matching: BipartiteGraphMatching):
    for vertex_idx in range(1, len(altng_chain) - 1, 2):
        right_vrtx, left_vrtx = altng_chain[vertex_idx], altng_chain[vertex_idx + 1]
        matching.remove_edge(left_vrtx, right_vrtx)
    
    for vertex_idx in range(0, len(altng_chain) - 1, 2):
        left_vrtx, right_vrtx = altng_chain[vertex_idx], altng_chain[vertex_idx + 1]
        matching.add_edge(left_vrtx, right_vrtx)
    
        


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
