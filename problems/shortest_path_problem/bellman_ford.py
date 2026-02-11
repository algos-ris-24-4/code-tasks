from problems.shortest_path_problem import INF, ShortestPath
from problems.shortest_path_problem.errors.error_message_enum import ErrorMessageEnum


class NegativeLoopBellmanFordError(RuntimeError):
    def __init__(self, last_updated_vertex_idx, predecessors):
        self.last_updated_vertex_idx = last_updated_vertex_idx
        self.predecessors = predecessors
        super().__init__(ErrorMessageEnum.NEGATIVE_LOOP)


def get_shortest_path(
    dist_matrix: list[list[int]], source_idx: int, target_idx: int
) -> ShortestPath:
    """
    Вычисляет кратчайший путь между двумя вершинами графа с использованием алгоритма Беллмана-Форда.

    :param dist_matrix: Квадратная матрица расстояний, где `dist_matrix[i][j]` представляет вес ребра (i, j).
                        Если между вершинами нет прямого пути, значение `None`.
    :type dist_matrix: list[list[int]]
    :param source_idx: Индекс начальной вершины.
    :type source_idx: int
    :param target_idx: Индекс целевой вершины.
    :type target_idx: int
    :return: Объект `ShortestPath`, содержащий:
             - `distance`: минимальное расстояние от `source_idx` до `target_idx` (или `None`, если путь недостижим).
             - `path`: список вершин, представляющий кратчайший путь (пустой, если путь отсутствует).
    :rtype: ShortestPath
    :raises ValueError: Если входные параметры некорректны.
    :raises NegativeLoopBellmanFordError: Если в графе обнаружен цикл отрицательной стоимости.
    """
    __validate_params(dist_matrix, source_idx, target_idx)
    if source_idx == target_idx:
        return ShortestPath(0, [])
    distances_from_source, predecessors = bellman_ford(dist_matrix, source_idx)
    if distances_from_source[target_idx] == INF:
        return ShortestPath(None, [])
    shortest_path = restore_path(predecessors, source_idx, target_idx)
    return ShortestPath(distances_from_source[target_idx], shortest_path)


def bellman_ford(
    dist_matrix: list[list[int]], source_idx: int
) -> tuple[list[int], list[int]]:
    """
    Реализует алгоритм Беллмана-Форда для вычисления кратчайших расстояний от исходной вершины до всех остальных.

    :param dist_matrix: Квадратная матрица расстояний между вершинами графа.
    :type dist_matrix: list[list[int]]
    :param source_idx: Индекс исходной вершины.
    :type source_idx: int
    :return: Список кратчайших расстояний от исходной вершины до каждой другой вершины. Если вершина недостижима,
        её расстояние будет равно INF.
        Список предшествующих вершин для восстановления кратчайшего пути.
    :rtype: tuple[list[int], list[int]]

    :raises NegativeLoopBellmanFordError: Если в графе обнаружен цикл отрицательной стоимости.
    """
    pass


def restore_path(
    predecessors: list[int], source_idx: int, target_idx: int
) -> list[int]:
    """
    Восстанавливает путь от исходной вершины до целевой, используя информацию о предшествующих вершинах.

    :param predecessors: Список предшествующих вершин для восстановления кратчайшего пути.
    :type predecessors: list[int]
    :param source_idx: Индекс исходной вершины.
    :type source_idx: int
    :param target_idx: Индекс целевой вершины.
    :type target_idx: int
    :return: Список индексов вершин, представляющих кратчайший путь от исходной до целевой вершины.
    :rtype: list[int]
    """
    pass


def __validate_params(dist_matrix: list[list[int]], source_idx: int, target_idx: int):
    """
    Проверяет корректность входных параметров для алгоритма поиска кратчайшего пути.

    Этот метод выполняет валидацию матрицы расстояний и индексов начальной и целевой вершин.
    Если параметры не соответствуют требованиям, выбрасывается исключение ValueError с соответствующим сообщением.

    Параметры:
        dist_matrix (list[list[int]]): Матрица расстояний, где каждый элемент — это либо неотрицательное целое число, либо `None`.
                                       Матрица должна быть квадратной и удовлетворять условиям, указанным в `__validate_matrix`.
        source_idx (int): Индекс исходной вершины. Должен быть целым числом от 0 до размера матрицы (не включительно).
        target_idx (int): Индекс целевой вершины. Должен быть целым числом от 0 до размера матрицы (не включительно).

    Исключения:
        ValueError: Выбрасывается в следующих случаях:
            - Если `dist_matrix` не соответствует требованиям (проверяется в `__validate_matrix`).
            - Если `source_idx` не является целым числом или выходит за границы допустимого диапазона (от 0 до порядка матрицы).
            - Если `target_idx` не является целым числом или выходит за границы допустимого диапазона (от 0 до порядка матрицы).
    """
    __validate_matrix(dist_matrix)

    order = len(dist_matrix)
    if not isinstance(source_idx, int) or source_idx < 0 or source_idx >= order:
        raise ValueError(ErrorMessageEnum.WRONG_SRC)
    if not isinstance(target_idx, int) or target_idx < 0 or target_idx >= order:
        raise ValueError(ErrorMessageEnum.WRONG_TRG)


def __validate_matrix(matrix: list[list[int]]) -> None:
    """
    Проверяет корректность матрицы расстояний.

    Этот метод выполняет валидацию матрицы расстояний для алгоритма поиска кратчайшего пути.
    Если матрица не соответствует требованиям, выбрасывается исключение ValueError с соответствующим сообщением.

    Параметры:
        matrix (list[list[int]]): Матрица расстояний, где каждый элемент — это либо неотрицательное целое число, либо `None`.
                                  Матрица должна быть квадратной и не содержать отрицательных значений.

    Исключения:
        ValueError: Выбрасывается в следующих случаях:
            - Если `matrix` не является списком.
            - Если `matrix` пуста.
            - Если строки `matrix` не являются списками.
            - Если `matrix` не является квадратной матрицей (число строк не равно числу столбцов).
            - Если в `matrix` содержатся значения, не являющиеся неотрицательными целыми числами или `None`.
    """
    if not isinstance(matrix, list):
        raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
    if not matrix:
        raise ValueError(ErrorMessageEnum.EMPTY_MATRIX)
    if not isinstance(matrix[0], list):
        raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
    if not matrix[0]:
        raise ValueError(ErrorMessageEnum.EMPTY_MATRIX)

    rows_cnt = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != rows_cnt:
            raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
        for value in row:
            if not isinstance(value, (int, type(None))):
                raise ValueError(ErrorMessageEnum.WRONG_MATRIX)


def main():
    matrix = [[0, None, None], [1, 0, None], [None, 1, 0]]
    src = 2
    trg = 0

    print("Исходная матрица")
    for row in matrix:
        print(row)

    result = get_shortest_path(matrix, src, trg)
    print(f"\nКратчайшее расстояние между вершинами {src} и {trg} составляет:")
    print(result.distance)
    print("Путь:")
    print(result.path)


if __name__ == "__main__":
    main()
