"""
rename this to in-place quick sort. Ya que Lomuto no es 3 way partition

"""


def three_way_partition(
    list_, mid_value: int, start=0, end=None
) -> ("low:int", "high:int"):
    """
    >>> partition = three_way_partition
    >>> l = [9, 5, 5, 0, 9, 0, 0, 5, 0, 9, 5]
    >>> low, high = partition(l, 5)
    >>> low
    4
    >>> high
    7
    >>> l
    [0, 0, 0, 0, 5, 5, 5, 5, 9, 9, 9]

                 ^           ^
                low         high

    more general than flag problem:

    >>> l = [8, 5, 3, 5, 9, 0, 2, 1, 7, 5, 5]
    >>> r = partition(l, 5)
    >>> l
    [3, 0, 2, 1, 5, 5, 5, 5, 7, 9, 8]
    >>> r
    (4, 7)

    It is stable? lt part yes, be no
    """
    if end is None:
        end = len(list_) - 1
    low = mid = start
    high = end
    while mid <= high:
        if list_[mid] < mid_value:
            list_[low], list_[mid] = list_[mid], list_[low]
            low += 1
            mid += 1
        elif list_[mid] > mid_value:
            list_[high], list_[mid] = list_[mid], list_[high]
            high -= 1
        else:
            mid += 1
    return low, high


def quick_sort_3partition(sorting: list, left: int, right: int) -> None:
    """ "
    Python implementation of quick sort algorithm with 3-way partition.
    The idea of 3-way quick sort is based on "Dutch National Flag algorithm".

    :param sorting: sort list
    :param left: left endpoint of sorting
    :param right: right endpoint of sorting
    :return: None

    Examples:
    >>> array1 = [5, -1, -1, 5, 5, 24, 0]
    >>> quick_sort_3partition(array1, 0, 6)
    >>> array1
    [-1, -1, 0, 5, 5, 5, 24]
    >>> array2 = [9, 0, 2, 6]
    >>> quick_sort_3partition(array2, 0, 3)
    >>> array2
    [0, 2, 6, 9]
    >>> array3 = []
    >>> quick_sort_3partition(array3, 0, 0)
    >>> array3
    []
    """
    if right <= left:
        return

    # any other could also work
    pivot = sorting[left]

    low, high = three_way_partition(sorting, pivot, start=left, end=right)
    quick_sort_3partition(sorting, left, low - 1)
    quick_sort_3partition(sorting, high + 1, right)


def quick_sort_lomuto_partition(sorting: list, left: int, right: int) -> None:
    """
    A pure Python implementation of quick sort algorithm(in-place)
    with Lomuto partition scheme:
    https://en.wikipedia.org/wiki/Quicksort#Lomuto_partition_scheme

    :param sorting: sort list
    :param left: left endpoint of sorting
    :param right: right endpoint of sorting
    :return: None

    Examples:
    >>> nums1 = [0, 5, 3, 1, 2]
    >>> quick_sort_lomuto_partition(nums1, 0, 4)
    >>> nums1
    [0, 1, 2, 3, 5]
    >>> nums2 = []
    >>> quick_sort_lomuto_partition(nums2, 0, 0)
    >>> nums2
    []
    >>> nums3 = [-2, 5, 0, -4]
    >>> quick_sort_lomuto_partition(nums3, 0, 3)
    >>> nums3
    [-4, -2, 0, 5]
    """
    if left < right:
        pivot_index = right
        pivot_index_final = lomuto_partition(sorting, pivot_index, left, right)
        quick_sort_lomuto_partition(sorting, left, pivot_index_final - 1)
        quick_sort_lomuto_partition(sorting, pivot_index_final + 1, right)


# TODO: puedo separar by_value y by_pivot
def lomuto_partition(
    sorting: list, pivot_index: int, start: int = 0, end: int = None
) -> int:
    """
    Returns the new pivot position. So that bigger or equal elements to the right.

    >>> list_unsorted = [7, 3, 5, 4, 1, 8, 6]

    Choose pivot l[3] == 4

    >>> l = list_unsorted.copy()
    >>> l[3]
    4
    >>> lomuto_partition(l, 3)
    2
    >>> l
    [3, 1, 4, 6, 7, 8, 5]

    2 is the definitive position of the pivot
    Notice that is not stable. Aun que parece que la parte lt sí.

    Corner cases:
    >>> l = list_unsorted.copy()

    pivot l[4] == 8 == max(l)

    or

    >>> max(l)
    8
    >>> l[5]
    8

    >>> lomuto_partition(l, 5)
    6

    >>> l = list_unsorted.copy()
    >>> min(l)
    1
    >>> l[4]
    1
    >>> lomuto_partition(l, 4)
    0

    Out of bounds ? -> imposible por el pivot. Más bien sería el dutch algorithm
    """
    if end is None:
        end = len(sorting) - 1
    pivot = sorting[pivot_index]

    # en realidad no hace falta guardar pivot...
    sorting[end], sorting[pivot_index] = sorting[pivot_index], sorting[end]
    store_index = start  # rename first bigger_or_equal. first_be
    for i in range(start, end):
        if sorting[i] < pivot:
            sorting[store_index], sorting[i] = sorting[i], sorting[store_index]
            store_index += 1
    sorting[end], sorting[store_index] = sorting[store_index], sorting[end]
    return store_index


# from snoop import snoop
# @snoop
def hoare_partition_by_value(
    array: list, pivot_value: int, start: int = 0, end: int = None
):
    """
    >>> list_unsorted = [7, 3, 5, 4, 1, 8, 6]

    >>> array = list_unsorted.copy()
    >>> hoare_partition_by_value(array, 5)
    3
    >>> array
    [1, 3, 4, 5, 7, 8, 6]


    >>> hoare_partition_by_value(list_unsorted.copy(), 0)
    0
    >>> hoare_partition_by_value(list_unsorted.copy(), 1)
    0
    >>> hoare_partition_by_value(list_unsorted.copy(), 2)
    1
    >>> hoare_partition_by_value(list_unsorted.copy(), 8)
    6
    >>> hoare_partition_by_value(list_unsorted.copy(), 9)
    7

    TODO: test len=0,1,2
    """
    if end is None:
        end = len(array) - 1

    # invariant: all(i < pivot_value  for i in array[start : last_lt])
    last_lt = start  # -1?
    # invariant: all(i >= pivot_value  for i in array[first_ge+1 :end])
    # lllllluuuuuurrrrrr
    #       ^    ^
    #       |    |
    #    last_array  first_be
    first_ge = end

    def swap(i1, i2):
        array[i1], array[i2] = array[i2], array[i1]

    # while last_lt<first_ge-1:
    # while first_ge-last_lt > 1:
    while True:
        while array[last_lt] < pivot_value:
            last_lt += 1
            if last_lt > end:
                # signal that lt subarray is empty with out of bounds
                return end + 1
        while (
            array[first_ge] >= pivot_value
        ):  # TODO: por qué en todos no es inclusiva esta comparación? Entre ellos donald knuth y wikipedia
            first_ge -= 1
            if first_ge < start:
                return start

        # if first_ge-last_lt > 1:
        if last_lt > first_ge:
            break

        swap(last_lt, first_ge)

        last_lt += 1
        first_ge -= 1

    return first_ge + 1
    # return last_lt


def hoare_partition_by_pivot(array: list, pivot_index, start=0, end=None):
    """
    Setup
    >>> import random
    >>> array_unsorted = [random.randrange(100) for _ in range(1000)]
    >>> array = array_unsorted.copy()
    >>> pivot_index = random.randrange(len(array))
    >>> pivot_value = array[pivot_index]

    Execution
    >>> new_pivot_index = hoare_partition_by_pivot(array, pivot_index)

    Validation
    >>> array[new_pivot_index] == array_unsorted[pivot_index]
    True
    >>> all(i <  pivot_value for i in array[:new_pivot_index])
    True
    >>> all(i >= pivot_value for i in array[new_pivot_index:])
    True
    """
    # TODO: move test to main? to prove all partitions-> not in CI. Move to module docstring?

    if end is None:
        end = len(array) - 1

    def swap(i1, i2):
        array[i1], array[i2] = array[i2], array[i1]

    pivot_value = array[pivot_index]

    swap(pivot_index, end)
    ge = hoare_partition_by_value(array, pivot_value, start=start, end=end - 1)
    swap(
        end, ge
    )  # TODO if out of bounds? -> index error. Bueno, con end+1 esté dentro de lista... no. Bueno, en realidad (end+1)-1 hace un swap en el mismo sitio.
    return ge


# hoare_partition.__doc__ = lomuto_partition.__doc__.replace('lomuto', 'hoare')

import random


def quicksort_hoare(array: list, start=0, end=None):
    """
    Quicksort using the Hoare partition scheme:
    - https://en.wikipedia.org/wiki/Quicksort#Hoare_partition_scheme
    - The Art of Computer Programming, Volume 3: Sorting and Searching, Section 5.2.2: Sorting by Exchanging
    """
    if end is None:
        end = len(array) - 1

    if end + 1 - start <= 1:
        return
    pivot_index = random.randrange(start, end)
    pivot_index_final = hoare_partition_by_pivot(
        array, pivot_index, start=start, end=end
    )
    quicksort_hoare(array, start, pivot_index_final - 1)
    quicksort_hoare(array, pivot_index_final + 1, end)


# TODO: rename l -> array?
# from snoop import snoop
# @snoop
def quicksort_hoare2(l, start=0, end=None):
    """
    este es el de wikipedia, que para mi contiene un bug.

    >>> import random
    >>> random.seed(0)
    >>> l = [1, 1]
    >>> quicksort_hoare2(l)
    """
    if end is None:
        end = len(l) - 1

    if end + 1 - start <= 1:
        return

    pivot_value = random.choice(l[start : end + 1])
    greater_or_equal = hoare_partition_by_value(l, pivot_value, start=start, end=end)
    quicksort_hoare2(l, start, greater_or_equal)  # Note index is now included
    quicksort_hoare2(l, greater_or_equal + 1, end)

    # The next causes infinite recursion when l = [1, 1]
    # sin embargo, parecía lo más rápido, ya que el pivote lo pone en una posición incorrecta.
    # ESTÁ mal, si el indice no es el pivote (lo más probable) ese elemento no estará en la parte buena
    # quicksort_hoare2(l, start, greater_or_equal-1)
    # quicksort_hoare2(l, greater_or_equal, end) # Note index is now included


def test_quicksort():
    import random

    random.seed(0)
    l_unsorted = [random.randrange(100) for _ in range(10)]
    print(l_unsorted)
    for algorithm in [
        quicksort_hoare,
        # quicksort_hoare2
    ]:
        l = l_unsorted.copy()
        algorithm(l)
        assert l == sorted(l_unsorted)


def test_parition_by_value():
    import random

    l_unsorted = [random.randrange(100) for _ in range(1000)]
    l = l_unsorted.copy()
    pivot_value = random.choice(l)
    greater_equal = hoare_partition_by_value(l, pivot_value)

    assert all(i < pivot_value for i in l[:greater_equal])
    assert all(i >= pivot_value for i in l[greater_equal:])


def three_way_radix_quicksort(sorting: list) -> list:
    """
    Three-way radix quicksort:
    https://en.wikipedia.org/wiki/Quicksort#Three-way_radix_quicksort
    First divide the list into three parts.
    Then recursively sort the "less than" and "greater than" partitions.

    >>> three_way_radix_quicksort([])
    []
    >>> three_way_radix_quicksort([1])
    [1]
    >>> three_way_radix_quicksort([-5, -2, 1, -2, 0, 1])
    [-5, -2, -2, 0, 1, 1]
    >>> three_way_radix_quicksort([1, 2, 5, 1, 2, 0, 0, 5, 2, -1])
    [-1, 0, 0, 1, 1, 2, 2, 2, 5, 5]
    """
    if len(sorting) <= 1:
        return sorting
    return (
        three_way_radix_quicksort([i for i in sorting if i < sorting[0]])
        + [i for i in sorting if i == sorting[0]]
        + three_way_radix_quicksort([i for i in sorting if i > sorting[0]])
    )


if __name__ == "__main__":
    import doctest

    # doctest.testmod(verbose=True)

    # user_input = input("Enter numbers separated by a comma:\n").strip()
    # unsorted = [int(item) for item in user_input.split(",")]
    # quick_sort_3partition(unsorted, 0, len(unsorted) - 1)
    # print(unsorted)
