from collections import namedtuple
from assignment_problem.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph_matching import BipartiteGraphMatching
from network_flow.min_cost_flow_calculator import MinCostFlowCalculator


AssignmentSolution = namedtuple("AssignmentSolution", ["cost", "assignments"])
NetworkMatrices = namedtuple("NetworkMatrices", ["capacity_matrix", "cost_matrix"])

def get_assignments(cost_matrix: list[list[int | float]]) -> AssignmentSolution:
    """
    Решает задачу о назначениях с использованиемалгоритма поиска 
    максимального потока минимальной стоимости.

    Задача заключается в нахождении совершенного паросочетания "исполнителей" (строки)
    и "задач" (столбцы), минимизирующей суммарную стоимость выполнения.
    Предполагается, что входная матрица квадратная (число исполнителей равно числу задач).

    :param cost_matrix: Квадратная матрица стоимостей размера n×n,
                        где cost_matrix[i][j] — стоимость назначения i-го исполнителя на j-ю задачу.
    :return: Объект AssignmentSolution, содержащий минимальную суммарную стоимость
             и список пар (i, j), представляющих оптимальные назначения.
    :raises ValueError: Если матрица некорректна (неквадратная, пустая, содержит недопустимые значения).
    """
    _validate_matrix(cost_matrix)
    matching = get_min_cost_perfect_matching(cost_matrix)
    total_cost = 0
    assignments = matching.get_matching()
    for row_idx, col_idx in assignments:
        total_cost += cost_matrix[row_idx][col_idx]

    return AssignmentSolution(total_cost, assignments)


def get_network_matrices(assignment_matrix: list[list[int | float]]) -> NetworkMatrices:
    """
    Преобразует матрицу назначений в матрицы пропускных способносткй и стоимостей с добавлением источника и стока 
    для построения сети для алгоритма поиска макс. потока мин. стоимости
    """
    order_asnm_matr = len(assignment_matrix)
    order_result = (order_asnm_matr * 2) + 2 # + источник и сток

    capacity_matr: list[list[int]] = [[0] * order_result for _ in range(order_result)]
    cost_matr: list[list[int]] = [[0] * order_result for _ in range(order_result)]

    # заполнение дуг источник -> вершины левой доли
    src_idx = 0
    for col_idx in range(src_idx + 1, order_asnm_matr + 1): 
        capacity_matr[src_idx][col_idx] = 1

    # заполнение дуг вершины правой доли -> сток
    trg_idx = order_result - 1
    for row_idx in range(order_asnm_matr + 1, trg_idx):
        capacity_matr[row_idx][trg_idx] = 1

    # заполнение дуг полного двудольного графа
    for row_idx in range(order_asnm_matr):
        edge_src = row_idx + 1
        for col_idx in range(order_asnm_matr):
            edge_trg = 1 + order_asnm_matr + col_idx
            capacity_matr[edge_src][edge_trg] = 1
            cost_matr[edge_src][edge_trg] = assignment_matrix[row_idx][col_idx]

    return NetworkMatrices(capacity_matr, cost_matr)
    



def get_min_cost_perfect_matching(assignment_matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Возвращает совершенное паросочетание с минимальной стоимостью, найденное с использованием алгоритма поиска 
    максимального потока минимальной стоимости.

    :param assignment_matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type assignment_matrix: list[list[int|float]]
    :return: Совершенное паросочетание с минимальной стоимостью.
    :rtype: BipartiteGraphMatching
    """

    # добавление источника и стока
    net_matrices = get_network_matrices(assignment_matrix)
    capacity_matrix: list[list[int]] = net_matrices.capacity_matrix
    cost_matrix: list[list[int]] = net_matrices.cost_matrix

    calculator = MinCostFlowCalculator(capacity_matrix, cost_matrix)
    flow_matrix = calculator.flow_matrix
    matching = BipartiteGraphMatching(len(assignment_matrix))   

    exec_start_pos = 1
    task_start_pos = len(assignment_matrix) + 1

    # добавление в пустое паросочетание ребра из полученной flow_matrix
    for number_executor in range(len(assignment_matrix)):
        executor_idx = exec_start_pos + number_executor

        for number_task in range(len(assignment_matrix)):
            task_idx = task_start_pos + number_task

            if flow_matrix[executor_idx][task_idx] > 0:
                matching.add_edge(number_executor,number_task)
                break

    return matching

def _validate_matrix(matrix: list[list[int | float]]) -> None:
    if (
        not matrix
        or not isinstance(matrix, list)
        or not matrix[0]
        or not isinstance(matrix[0], list)
    ):
        raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
    row_cnt = len(matrix[0])
    for row in matrix:
        if len(row) != row_cnt:
            raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
        for value in row:
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(ErrorMessageEnum.WRONG_MATRIX)


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

    matching = get_min_cost_perfect_matching(matrix)
    
    result = get_assignments(matrix)
    print("\nРешение задачи о назначениях")
    print(f"Стоимость назначения: {result.cost}")
    print("Назначения: ")
    for assignment in result.assignments:
        print(assignment)
