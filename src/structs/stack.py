from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    """
    A generic stack implementation.
    
    """
    def __init__(self) -> None:
        self.items: list[T] = []

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from an empty stack")

    def peek(self) -> T:
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from an empty stack")

    def size(self) -> int:
        return len(self.items)
