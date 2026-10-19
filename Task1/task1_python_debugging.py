from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def unique_values(items: Iterable[T]) -> list[T]:
    """
    Return unique values in their original order.    
    """
    result: list[T] = []

    for item in items:
        if item not in result:
            result.append(item)

    return result


if __name__ == "__main__":
    print(unique_values([1, 2, 2, 3]))
    # Expected: [1, 2, 3]