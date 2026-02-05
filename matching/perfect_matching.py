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
    
    order = bipartite_graph.order
    matching = BipartiteGraphMatching(order)
    
    while not matching.is_perfect:        
        start_node = -1
        for left_node in range(order):
            if not matching.is_left_covered(left_node):
                start_node = left_node
                break   

        result = find_end_node(start_node,matching,bipartite_graph)
        path_end = result[0]
        parents = result[1]
        if path_end != -1:
            repaint(path_end, parents,matching, bipartite_graph)
        else:          
            raise PerfectMatchingError(ErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH)

    return matching

def repaint(path_end, parents, matching, bipartite_graph):
    """Принимает последнюю точку пути а также словарь пути и перекрашивает цепь"""
    curr_right = path_end
     #Восстановление пути
    while curr_right is not None:
        parent_left = parents[curr_right]
        next_right_in_path = None

        if matching.is_left_covered(parent_left):                    
            next_right_in_path = matching.get_right_match(parent_left)
            matching.remove_edge(parent_left, next_right_in_path)
        
        matching.add_edge(parent_left, curr_right)
        curr_right = next_right_in_path   

def find_end_node(start_node : int, matching,bipartite_graph):
    """Находит последний узел а также путь цепочки"""
    queue = deque([start_node])
    #Хранит левую вершину из которой пришли в правую 
    parents: dict[int, int] = {}        
    path_end = -1   
    
    while queue:
            left_node = queue.popleft() 
            neighbors = bipartite_graph.right_neighbors(left_node)            
            for right_node in neighbors:
                if right_node in parents:
                    continue
                parents[right_node] = left_node                
                if not matching.is_right_covered(right_node):
                    path_end = right_node
                    return [path_end, parents]
                else:
                    next_left = matching.get_left_match(right_node)
                    queue.append(next_left)
    return [path_end, parents]
        



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
