class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def to_list(self):
        ll_array = []
        if self.head is not None:
            node = self.head
            while node:
                ll_array.append(node.data)
                node = node.next_node
        return ll_array

    def print_ll(self):
        ll_string = ""
        node = self.head
        while node:
            ll_string += f" {str(node.data)} ->"
            node = node.next_node

        ll_string += " None"
        print(ll_string)

    def insert_at_head(self, data):
        if self.head is None:
            self.head = Node(data, None)
            self.tail = self.head
            return
        new_node = Node(data, self.head)
        self.head = new_node

    def insert_at_end(self, data):
        if self.head is None:
            self.insert_at_head(data)
            return
        self.tail.next_node = Node(data, None)
        self.tail = self.tail.next_node

    def get_by_id(self, id):
        if self.head is None:
            return
        node = self.head
        while node:
            if isinstance(node.data, dict):
                if node.data['id'] is int(id):
                    return node.data
            node = node.next_node
        return None