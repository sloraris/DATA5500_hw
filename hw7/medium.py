# *insert large magnifying glass and detective hat*

def wheresWaldo(node, key):
    if node == None:
        # Error 404: Waldo not found
        return False
    if node == key:
        # Error 040: Waldo not hidden
        return True

    if key < node.key:
        return wheresWaldo(node.left, key)
    if node.key < key:
        return wheresWaldo(node.right, key)
