from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.error_message_enum import ErrorMessageEnum


def get_max_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит максимальное по мощности паросочетание в двудольном графе с долями равной мощности.

    Алгоритм начинает с пустого паросочетания и последовательно ищет увеличивающие
    (чередующиеся) пути относительно текущего паросочетания. Каждый найденный путь
    используется для увеличения мощности паросочетания на единицу. Процесс завершается,
    когда увеличивающих путей больше не существует — в этот момент паросочетание
    становится максимальным (по теореме Бержа).

    Для поиска увеличивающих путей используется «волновой метод»:
    - нулевой фронт волны составляют все свободные вершины левой доли;
    - с чётных фронтов (левая доля) переходим к смежным вершинам правой доли
      по рёбрам, не входящим в текущее паросочетание;
    - с нечётных фронтов (правая доля) переходим к вершинам левой доли только
      по рёбрам текущего паросочетания.

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :return: Объект BipartiteGraphMatching, представляющий максимальное паросочетание.
    """
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)

    order = bipartite_graph.order
    matching = BipartiteGraphMatching(order)

    # Пока удаётся найти увеличивающую цепь, продолжаем увеличивать паросочетание.
    while True:
        path = _find_augmenting_path(bipartite_graph, matching)
        if not path:
            break
        _augment_matching(matching, path)

    return matching


def _find_augmenting_path(
    bipartite_graph: BipartiteGraph,
    matching: BipartiteGraphMatching,
) -> list[tuple[int, int]]:
    """
    Ищет увеличивающую (чередующуюся) цепь с помощью волнового метода.

    Нулевой фронт волны — все свободные вершины левой доли.
    С чётных фронтов (левая доля) двигаемся по рёбрам, не входящим в текущее
    паросочетание, к правой доле. С нечётных фронтов (правая доля) двигаемся
    по рёбрам текущего паросочетания обратно к левой доле.

    Как только достигаем свободную вершину правой доли, получаем увеличивающую цепь.
    """
    order = bipartite_graph.order

    #нулевой фронт волны: все свободные левые вершины
    free_left = [i for i in range(order) if not matching.is_left_covered(i)]
    if not free_left:
        return []

    #для восстановления пути храним предка каждой посещённой вершины.
    #вершины кодируем как ('L' или 'R', индекс).
    parent: dict[tuple[str, int], tuple[str, int] | None] = {}

    queue: deque[tuple[str, int]] = deque()
    visited_left: set[int] = set()
    visited_right: set[int] = set()

    for v in free_left:
        node = ("L", v)
        queue.append(node)
        parent[node] = None
        visited_left.add(v)

    while queue:
        side, idx = queue.popleft()

        if side == "L":
            #чётный фронт: вершины левой доли.
            #идём по рёбрам, которые не входят в текущее паросочетание.
            for right in bipartite_graph.right_neighbors(idx):
                if right in visited_right:
                    continue

                #пропускаем рёбра, которые уже входят в паросочетание с этой левой вершиной,
                # чтобы сохранялось чередование.
                if matching.is_left_covered(idx) and matching.get_right_match(idx) == right:
                    continue

                visited_right.add(right)
                right_node = ("R", right)
                parent[right_node] = (side, idx)

                #если правая вершина свободна — увеличивающая цепь найдена.
                if not matching.is_right_covered(right):
                    return _reconstruct_path(parent, right_node)

                #иначе переходим по рёбру из паросочетания к соответствующей левой вершине
                left_match = matching.get_left_match(right)
                if left_match not in visited_left:
                    visited_left.add(left_match)
                    left_node = ("L", left_match)
                    parent[left_node] = right_node
                    queue.append(left_node)

        else:
            #нечётный фронт (правая доля) явно не обрабатываем: переход по
            #рёбрам текущего паросочетания уже учтён в блоке выше.
            continue

    #увеличивающей цепи не существует
    return []


def _reconstruct_path(
    parent: dict[tuple[str, int], tuple[str, int] | None],
    end_node: tuple[str, int],
) -> list[tuple[int, int]]:
    """
    Восстанавливает чередующуюся цепь по таблице предков.

    :param parent: Словарь предков вершин ('L'/'R', idx).
    :param end_node: Конечная вершина пути (свободная правая вершина).
    :return: Список рёбер (левая_вершина, правая_вершина) вдоль пути.
    """
    nodes: list[tuple[str, int]] = []
    current = end_node

    while current is not None:
        nodes.append(current)
        current = parent[current]

    nodes.reverse()

    edges: list[tuple[int, int]] = []
    for (side_u, idx_u), (side_v, idx_v) in zip(nodes, nodes[1:]):
        if side_u == "L" and side_v == "R":
            edges.append((idx_u, idx_v))
        elif side_u == "R" and side_v == "L":
            edges.append((idx_v, idx_u))

    return edges


def _augment_matching(
    matching: BipartiteGraphMatching,
    augmenting_path: list[tuple[int, int]],
) -> None:
    """
    Увеличивает паросочетание вдоль найденной чередующейся цепи.

    Рёбра, которые уже входят в паросочетание, удаляются;
    рёбра, которых в паросочетании не было, добавляются.
    В результате мощность паросочетания увеличивается на 1.
    """
    for left, right in augmenting_path:
        in_matching = matching.is_left_covered(left) and matching.get_right_match(left) == right

        if in_matching:
            #ребро принадлежит текущему паросочетанию — удаляем его.
            matching.remove_edge(left, right)
        else:
            #ребро не принадлежит паросочетанию — добавляем его.
            #в корректной увеличивающей цепи конфликтов быть не должно,
            #но на всякий случай удаляем возможные старые рёбра.
            if matching.is_left_covered(left):
                old_right = matching.get_right_match(left)
                matching.remove_edge(left, old_right)
            if matching.is_right_covered(right):
                old_left = matching.get_left_match(right)
                matching.remove_edge(old_left, right)

            matching.add_edge(left, right)
