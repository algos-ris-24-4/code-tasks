from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.error_message_enum import ErrorMessageEnum
from collections import deque


def get_max_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит максимальное по мощности паросочетание в двудольном графе с долями равной мощности.

    Алгоритм начинает с пустого паросочетания и последовательно ищет увеличивающие 
    (чередующиеся) пути относительно текущего паросочетания. Каждый найденный путь 
    используется для увеличения мощности паросочетания на единицу. Процесс завершается, 
    когда увеличивающих путей больше не существует — в этот момент паросочетание 
    становится максимальным (по теореме Бержа).

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :return: Объект BipartiteGraphMatching, представляющий максимальное паросочетание.
    """
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)
    
    matching = BipartiteGraphMatching(bipartite_graph.order)

    while True:
        parent = [-1] * bipartite_graph.order
        queue = deque()
        
        for left in range(bipartite_graph.order):
            if not matching.is_left_covered(left):
                queue.append(left)

        if not queue:
            break
        
        last_right = -1
        while queue and last_right == -1:
            leftNode = queue.popleft()
            
            for rightNode in bipartite_graph.right_neighbors(leftNode):
                if matching.get_right_match(leftNode) == rightNode:
                    continue
                
                if parent[rightNode] == -1:
                    parent[rightNode] = leftNode
                    
                if not matching.is_right_covered(rightNode):
                    last_right = rightNode
                    break
                else:
                    nextNode = matching.get_left_match(rightNode)
                    queue.append(nextNode)
        
        if last_right == -1:
            break
        
        rightNode = last_right
        while rightNode != -1:
            leftNode = parent[rightNode]
            oldRight = matching.get_right_match(leftNode)
            
            if oldRight != -1:
                matching.remove_edge(leftNode, oldRight)
            matching.add_edge(leftNode, rightNode)
            
            rightNode = oldRight
    
    return matching


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
    print(get_max_matching(bipartite_graph))
