from problems.sorting_problem.errors.error_message_template_enum import (
    ErrorMessageTemplateEnum,
)


def quick_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr.copy()

    pivot = arr[0]
    less = []
    equal = [pivot]
    greater = []

    for item in arr[1:]:
        try:
            if item < pivot:
                less.append(item)
            elif item > pivot:
                greater.append(item)
            else:
                equal.append(item)
        except TypeError:
            item_type = type(item).__name__
            pivot_type = type(pivot).__name__
            types = sorted([item_type, pivot_type], reverse=True)
            raise TypeError(
                ErrorMessageTemplateEnum.ERR_INCOMPARABLE_EMBEDDED_TYPES.format(
                    types[0], types[1]
                )
            )

    return quick_sort(less) + equal + quick_sort(greater)
