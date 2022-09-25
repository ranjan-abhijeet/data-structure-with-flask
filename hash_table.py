class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * table_size

    
    def custom_hash(self, key):
        hash_value = 0
        for i in key:
            hash_value += ord(i)
            hash_value = (hash_value * ord(i)) % self.table_size
        return hash_value

    def add_key_value(self, key, value):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        else:
            node = self.hash_table[hashed_key]
            while node.next_node:
                node = node.next_node

            node.next_node = Node(Data(key, value), None)
            
    def get_value(self, key):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.next_node is None:
                return self.hash_table[hashed_key].data.value
            while node.next_node:
                if node.data.key == key:
                    return node.data.value
                node = node.next_node
            if node.data.key == key:
                return node.data.value
        return None

    def print_table(self):
        print("{")
        if self.hash_table is not None:
            for i, val in enumerate(self.hash_table):
                if val is not None:
                    ll_string = ""
                    node = val
                    if node.next_node:
                        while node.next_node:
                            ll_string += (
                                            str(node.data.key) + ":" + str(node.data.value) + " -->  "
                                        )
                            node = node.next_node
                        ll_string += (str(node.data.key) + ":" + str(node.data.value) + " --> None")
                    
                        print(f"    [{i}] {ll_string}")
                    else:
                        print(f"    [{i}] {node.data.key}:{node.data.value}")
                else:
                    print(f"    [{i}] {val}")
        print("}")
