from .errors.error_message_template_enum import ErrorMessageTemplateEnum

def validate_list(items: list) -> None:
    """
    Выполняет валидацию входного списка для сортировки:
    - На вход подаётся не None;
    - На вход подаётся список;

    :param items: Объект для проверки.
    :raises ValueError: Если входной объект не является списком.
    """
    if items is None:
        raise ValueError(ErrorMessageTemplateEnum.ERR_INPUT_IS_NONE)
    if not isinstance(items, list):
        raise ValueError(ErrorMessageTemplateEnum.ERR_NOT_A_LIST)


def validate_comparison(elem1, elem2) -> None:
    try:
        _ = elem1 < elem2
    except TypeError:
        err_msg = ErrorMessageTemplateEnum.ERR_INCOMPARABLE_EMBEDDED_TYPES.format(
            type(elem2).__name__,
            type(elem1).__name__
        )
        raise TypeError(err_msg)


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
    left_lst = merge_sort_impl(items[:mid])
    right_lst = merge_sort_impl(items[mid:])

    return merge_lists(left_lst, right_lst)


def merge_lists(left_lst: list, right_lst: list) -> list:
    """
    Сливает два отсортированных списка в один.
    
    :param left_lst: Левая половина списка.
    :param right_lst: Правая половина списка.
    :return: Новый отсортированный список объединёный из left_lst и right_lst.
    """
    result = []
    lt_idx = rt_idx = 0

    while lt_idx < len(left_lst) and rt_idx < len(right_lst):
        lt_elem, rt_elem = left_lst[lt_idx], right_lst[rt_idx]
        validate_comparison(lt_elem, rt_elem)

        if lt_elem < rt_elem:
            result.append(lt_elem)
            lt_idx += 1
        else:
            result.append(rt_elem)
            rt_idx += 1

    result.extend(left_lst[lt_idx:])
    result.extend(right_lst[rt_idx:])

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
