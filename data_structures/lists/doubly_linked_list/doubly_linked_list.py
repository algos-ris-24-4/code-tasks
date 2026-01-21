from data_structures.lists.base_list import BaseList
from data_structures.lists.doubly_linked_list.doubly_list_node import DoublyListNode


class DoublyLinkedList(BaseList):
    """
    Реализация двусвязного списка.

    Атрибуты:
        head (DoublyListNode | None): ссылка на первый элемент списка.
        tail (DoublyListNode | None): ссылка на последний элемент списка.
        size (int): количество элементов в списке.
    """

    def __init__(self):
        """Создаёт пустой двусвязный список."""
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        """Добавляет элемент в конец списка."""
        new_node = DoublyListNode(value)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def appendleft(self, value):
        """Добавляет элемент в начало списка."""
        new_node = DoublyListNode(value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert(self, index, value):
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")

        if index == 0:
            self.appendleft(value)
            return
        if index == self.size:
            self.append(value)
            return

        current = self.head
        for _ in range(index):
            current = current.next

        new_node = DoublyListNode(value)
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        self.size += 1

    def remove(self, value):
        """Удаляет первый элемент с указанным значением."""
        current = self.head
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self.size -= 1
                return
            current = current.next
        raise ValueError("Value not found in list")

    def pop(self):
        """Удаляет и возвращает последний элемент."""
        if self.tail is None:
            raise IndexError("pop from empty list")
        value = self.tail.value
        if self.tail.prev:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            self.head = self.tail = None
        self.size -= 1
        return value

    def popleft(self):
        """Удаляет и возвращает первый элемент."""
        if self.head is None:
            raise IndexError("popleft from empty list")
        value = self.head.value
        if self.head.next:
            self.head = self.head.next
            self.head.prev = None
        else:
            self.head = self.tail = None
        self.size -= 1
        return value

    def index(self, value):
        """Возвращает индекс первого элемента с указанным значением или None."""
        current = self.head
        idx = 0
        while current:
            if current.value == value:
                return idx
            current = current.next
            idx += 1
        return None

    def __str__(self) -> str:
        """Возвращает строковое представление двусвязного списка."""
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " <-> ".join(values)

    def __len__(self):
        """Возвращает количество элементов в списке."""
        return self.size


    def __iter__(self):
        """Итерация по элементам списка слева направо."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __reversed__(self):
        """Итерация по элементам списка справа налево."""
        current = self.tail
        while current:
            yield current.value
            current = current.prev


if __name__ == "__main__":
    dll = DoublyLinkedList()

    dll.append(10)
    dll.append(20)
    dll.append(30)
    print("После добавления:", dll)

    dll.insert(0, 5)
    print("После вставки в начало:", dll)

    dll.insert(2, 15)
    print("После вставки в середину:", dll)

    dll.remove(20)
    print("После удаления 20:", dll)

    idx = dll.index(30)
    print(f"Индекс элемента 30: {idx}")

    print("Размер списка:", len(dll))

    print("Элементы списка:", [x for x in dll])

    print("Обратный обход:", [x for x in reversed(dll)])
