from enum import StrEnum

class SortingErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках сортировки."""

    INPUT_IS_NONE = "Входной аргумент не может быть None."
    NOT_A_LIST = "Входной аргумент должен быть списком."

def validate_list(items) -> None:
    """
    Выполняет валидацию входного списка для сортировки:
    - На вход подаётся не None;
    - На вход подаётся список;
    - Список не пустой и содержит больше двух элементов;                #Реализовано во внутренней реализации функции сортировки
    - Все объекты в списке сравнимы друг с другом;                      #Пока не реализовано 

    :param items: Объект для проверки.
    :raises TypeError: Если элементы списка несравнимы.                  #Пока не используется
    :raises ValueError: Если входной объект не является списком.
    """
    if items is None:
        raise ValueError(SortingErrorMessages.INPUT_IS_NONE)
    if not isinstance(items, list):
        raise ValueError(SortingErrorMessages.NOT_A_LIST)

def merge_sort_impl(items: list) -> list:
    """
    Рекурсивная сортировка слиянием - внутренняя реализация.

    Алгоритм делит список пополам, рекурсивно сортирует каждую половину,
    затем сливает отсортированные половины в единый список.

    :param items: Список элементов, поддерживающих операции сравнения.
    :return: Новый список, с отсортированными элементами.    
    """
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left_sorted = merge_sort_impl(items[:mid])
    right_sorted = merge_sort_impl(items[mid:])
    return merge(left_sorted, right_sorted)


def merge(left: list, right: list):
    """
    Сливает два отсортированных списка в один.
    
    :param left: Отсортированный список.
    :param right: Отсортированный список.
    :return: Новый отсортированный список объединёный из left и right.
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(items) -> list:
    """
    Рекурсивная сортировка слиянием - публичная функция.

    Алгоритм делит список пополам, рекурсивно сортирует каждую половину,
    затем сливает отсортированные половины в единый список.

    :param items: Список элементов.
    :return: Отсортированный список.
    :raises ValueError: Если входной аргумент равен None или не является списком.
    :raises TypeError: Если элементы списка несравнимы.                  #Пока не используется
    """
    validate_list(items)

    return merge_sort_impl(items)

def main():
    print("Пример сортировки ...")
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print(f"Исходный массив: {items}")
    print(f"Отсортированный массив: {merge_sort(items)}")


if __name__ == "__main__":
    main()
