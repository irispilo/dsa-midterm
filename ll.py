"""Lista doblemente enlazada no-circular."""


class Node:
    def __init__(self, data: any):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"(DATA: {self.data})"


class DoublyLinkedList:
    def __init__(self):
        self.start = None
        self.end = None

    def __repr__(self):
        nodes = ["START"]
        for node in self:
            nodes.append(str(node.data))
        nodes.append("NIL")
        return "\n" + " <--> ".join(nodes)

    def __iter__(self):
        node = self.start
        while node is not None:
            yield node
            node = node.next

    def __len__(self):
        length = 0
        for _ in self:
            length += 1
        return length

    def traverse(self):
        for node in self:
            print(node.data)

    def insert_at_end(self, element: Node):
        element.next = None
        element.prev = self.end
        if self.end is not None:
            self.end.next = element
        self.end = element
        if self.start is None:
            self.start = element

    def delete_node(self, element_data: any):
        for current in self:
            if current.data == element_data:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.start = current.next
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.end = current.prev
                return

    def search(self, element_data: any):
        for node in self:
            if node.data == element_data:
                return node
        return None
