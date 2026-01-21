from math import inf
from problems.tsp_problem.tsp_abs_solver import (
    AbstractTspSolver,
    TspSolution,
)
from generators.permutation_generator import generate_permutations


class BruteForceTspSolver(AbstractTspSolver):
    def get_tsp_solution(self) -> TspSolution:
        """Возвращает решение задачи коммивояжера в виде именованного кортежа с полями:
        - distance - кратчайшее расстояние,
        - path - список с индексами вершин на кратчайшем маршруте.
        """

        if self.order == 1:
            return TspSolution(0, [0])

        destinations = list(range(1, self.order))

        if not destinations:
            return TspSolution(None, [])

        all_permutations = generate_permutations(destinations)
        is_symmetric = True

        for row_idx in range(self.order): 
            for col_idx in range(row_idx + 1, self.order): 
                if self._dist_matrix[row_idx][col_idx] != self._dist_matrix[col_idx][row_idx]:
                    is_symmetric = False
                    break
            if not is_symmetric:
                break

        min_path_length = None
        shortest_path = []

        for current_permutation in all_permutations:
            if is_symmetric and len(current_permutation) > 0:
                if current_permutation[0] > current_permutation[-1]:
                    continue

            route = [0] + list(current_permutation) + [0]
            is_valid_route = True

            if self._dist_matrix[0][current_permutation[0]] is None:
                is_valid_route = False

            if is_valid_route:
                for position in range(len(current_permutation) - 1):
                    if self._dist_matrix[current_permutation[position]][current_permutation[position+1]] is None:
                        is_valid_route = False
                        break

            if is_valid_route:
                if self._dist_matrix[current_permutation[-1]][0] is None:
                    is_valid_route = False

            if is_valid_route:
                path_length = self.get_distance(self._dist_matrix, route)
                if min_path_length is None or path_length < min_path_length:
                    min_path_length = path_length
                    shortest_path = route

        if min_path_length is None:
            return TspSolution(None, [])

        return TspSolution(min_path_length, shortest_path)


if __name__ == "__main__":
    print("Пример решения задачи коммивояжёра\n\nМатрица расстояний:")
    matrix = [
        [None, 12.0, 9.0, 9.0, 12.0],
        [9.0, None, 8.0, 19.0, 15.0],
        [7.0, 1.0, None, 17.0, 11.0],
        [5.0, 9.0, 12.0, None, 16.0],
        [14.0, 6.0, 12.0, 22.0, None],
    ]
    for row in matrix:
        print(row)

    solver = BruteForceTspSolver(matrix)
    result = solver.get_tsp_solution()
    print(f"Минимальное расстояние: {result.distance}, " f"Маршрут: {result.path}")