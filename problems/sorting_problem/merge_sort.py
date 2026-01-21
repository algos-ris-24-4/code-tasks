from problems.sorting_problem.errors.error_message_template_enum import (
    ErrorMessageTemplateEnum,
)
def merge_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr.copy()

    mid = n // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    merged = []
    i = j = 0
    len_left, len_right = len(left), len(right)

    while i < len_left and j < len_right:
        try:
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        except TypeError:
            left_type = type(left[i]).__name__
            right_type = type(right[j]).__name__
            types = sorted([left_type, right_type], reverse=True)
            raise TypeError(
                ErrorMessageTemplateEnum.ERR_INCOMPARABLE_EMBEDDED_TYPES.format(
                    types[0], types[1]
                )
            )

    if i < len_left:
        merged.extend(left[i:])
    if j < len_right:
        merged.extend(right[j:])

    return merged