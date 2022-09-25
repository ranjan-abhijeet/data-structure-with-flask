class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def _insert_recursive(self, data, node):
        if data["id"] < node.data["id"]:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_recursive(data, node.left)
        elif data["id"] > node.data["id"]:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_recursive(data, node.right)
        else:
            return


    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_recursive(data, self.root)
            

    def _search_recursive(self, value, node):

        if value == node.data["id"]:
            return node.data

        elif value < node.data["id"] and node.left is not None:
            if value == node.left.data["id"]:
                return node.left.data                
            else:            
                return self._search_recursive(value, node.left)

        elif value > node.data["id"] and node.right is not None:
            if value == node.right.data["id"]:
                return node.right.data                
            else:            
                return self._search_recursive(value, node.right)

        return False

    def search(self, value):
        value = int(value)
        if self.root is None:
            return False    
        
        return self._search_recursive(value, self.root)