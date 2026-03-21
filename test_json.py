import json
import time
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from problems.knapsack_problem.genetic_solver import GeneticSolver

def test_from_json():
    json_path = Path(__file__).parent / 'large_hard_test.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    weights = data['problem']['weights']
    costs = data['problem']['costs']
    weight_limit = data['problem']['capacity']
    expected_cost = data['solution']['max_value']
    epochs = 200
    
    print(f"\nЗагрузка: {len(weights)} предметов")
    print(f"Лимит веса: {weight_limit}")
    
    solver = GeneticSolver(weights, costs, weight_limit)
    
    start = time.perf_counter()
    result = solver.get_knapsack(epoch_cnt=epochs, time_limit_sec=30.0)
    elapsed = time.perf_counter() - start
    
    total_weight = sum(weights[i] for i in result.items)
    total_cost = sum(costs[i] for i in result.items)
    
    print(f"\nОптимальная стоимость: {expected_cost}")
    print(f"Найденная стоимость:   {result.cost}")
    print(f"Точность:              {(result.cost / expected_cost) * 100:.1f}%")
    print(f"Вес решения:           {total_weight} / {weight_limit}")
    print(f"Предметов выбрано:     {len(result.items)}")
    print(f"Время выполнения:      {elapsed:.3f} сек")
    print(f"Количество поколений:  {epochs}")
    
    assert total_weight <= weight_limit, f"Перевес: {total_weight} > {weight_limit}"
    assert result.cost == total_cost, f"Несовпадение стоимости: {result.cost} != {total_cost}"
    assert result.cost >= expected_cost * 0.9, f"Точность ниже 90%"
    
if __name__ == '__main__':
    test_from_json()