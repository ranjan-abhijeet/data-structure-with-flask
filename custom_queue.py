class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node


class Queue:
    def __init__(self):
        self.head = None # head is the first item which will be removed
        self.tail = None # tail is the last item which was added

    def enqueue(self, data):
        if self.head is None and self.tail is None:
            node = Node(data, None)
            self.head = self.tail = node
            return
        
        self.tail.next_node = Node(data, None)
        self.tail = self.tail.next_node
        return

    def dequeue(self):
        if self.head is None:
            return
        
        removed = self.head
        self.head = self.head.next_node
        if self.head is None:
            self.tail = None

        return removed
        