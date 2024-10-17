# It's like Christmas tree shopping, but less jank and with fewer bungie cords

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insertNode(node, key):
    if node == None:
        return Node(key)

    if key < node.key:
        node.left = insertNode(node.left, key)
    elif node.key < key:
        node.right = insertNode(node.right, key)
