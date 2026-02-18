from collections import namedtuple

from problems.shortest_path_problem import INF, ShortestPath
from problems.shortest_path_problem.errors.error_message_enum import ErrorMessageEnum


def get_shortest_path(
    dist_matrix: list[list[int]], source_idx: int, target_idx: int
) -> ShortestPath:
    """
    Вычисляет кратчайший путь между двумя вершинами графа с использованием алгоритма Флойда-Уоршелла.

    :param dist_matrix: Квадратная матрица расстояний, где `dist_matrix[i][j]` представляет вес ребра (i, j).
                        Если между вершинами нет прямого пути, значение `None`.
    :type dist_matrix: list[list[int]]
    :param source_idx: Индекс начальной вершины.
    :type source_idx: int
    :param target_idx: Индекс целевой вершины.
    :type target_idx: int
    :return: Именованный кортеж `ShortestPath`, с полями:
             - `distance`: минимальное расстояние от `source_idx` до `target_idx` (или `None`, если путь недостижим).
             - `path`: список вершин, представляющий кратчайший путь (пустой, если путь отсутствует).
    :rtype: ShortestPath
    :raises ValueError: Если входные параметры некорректны.
    :raises RuntimeError: Если в графе обнаружен цикл отрицательной стоимости.
    """
    __validate_params(dist_matrix, source_idx, target_idx)
    if source_idx == target_idx:
        return ShortestPath(0, [])
    distances = __floyd_warshall(dist_matrix)
    if distances[source_idx][target_idx] == INF:
        return ShortestPath(None, [])
    shortest_path = __restore_path(dist_matrix, distances, source_idx, target_idx)
    return ShortestPath(distances[source_idx][target_idx], shortest_path)


def __floyd_warshall(dist_matrix: list[list[int]]) -> list[list[int]]:
  
    n = len(dist_matrix)

    dist: list[list[float]] = []
    for i in range(n):
        row: list[float] = []
        for j in range(n):
            value = dist_matrix[i][j]
            if i == j:
                row.append(0)
            elif value is None:
                row.append(INF)
            else:
                row.append(value)
        dist.append(row)

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[k][j] == INF:
                    continue
                new_dist = dist[i][k] + dist[k][j]
                if new_dist < dist[i][j]:
                    dist[i][j] = new_dist

    for i in range(n):
        if dist[i][i] < 0:
            raise RuntimeError(ErrorMessageEnum.NEGATIVE_LOOP)

    return dist


def __restore_path(
    dist_matrix: list[list[int]], dist: list[list[int]], source_idx: int, target_idx: int) -> list[int]:
    if dist[source_idx][target_idx] == INF:
        return []

    n = len(dist)

    def edge_weight(i: int, j: int) -> float:
        value = dist_matrix[i][j]
        if value is None:
            return INF
        return value

    def build_path(i: int, j: int) -> list[int]:
        if i == j:
            return [i]

        if edge_weight(i, j) == dist[i][j]:
            return [i, j]

        for k in range(n):
            if k == i or k == j:
                continue
            if dist[i][k] == INF or dist[k][j] == INF:
                continue
            if dist[i][k] + dist[k][j] == dist[i][j]:
                left = build_path(i, k)
                right = build_path(k, j)
                return left[:-1] + right

        raise ValueError("Не удалось восстановить путь")

    return build_path(source_idx, target_idx)


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
