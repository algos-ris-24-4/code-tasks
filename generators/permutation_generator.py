from typing import Any


def generate_permutations(items: list[Any]) -> list[list[Any]]:
    """Генерирует все варианты перестановок элементов указанного множества

    :param items: список элементов
    :raise TypeError: если параметр items не является списком
    :raise ValueError: если список элементов содержит дубликаты
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """

    if not isinstance(items, list):
        raise TypeError("Параметр items не является списком")
    
    if len(items) != len(set(items)):
        raise ValueError("Список элементов содержит дубликаты")
    
    if len(items) == 0:
        return []
    
    if len(items) == 1:
        return [items[:]]
    
    all_permutations = []
    prev_permutations = generate_permutations(items[:-1])
    current_element = items[-1]

    
    
    for permutation in prev_permutations:
        for position in range(len(permutation) + 1):
            new_permutation = permutation[:]
            new_permutation.insert(position, current_element)
            all_permutations.append(new_permutation)
            
    return all_permutations


def main():
    items = [1, 2, 3]
    print(generate_permutations(items))


if __name__ == "__main__":
    main()

    from typing import Any