class Node:
    def __init__(self, key):
        self.key = key      # The value stored in the node
        self.left = None    # Left child
        self.right = None   # Right child
        self.parent = None  # Parent node

class BST:
    def __init__(self):
        self.root = None  # Root of the BST

    def insert(self, key):
        new_node = Node(key)
        y = None
        x = self.root

        # Find the correct position for the new node
        while x is not None:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right

        new_node.parent = y

        # Insert the new node
        if y is None:
            self.root = new_node  # The tree was empty
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node

        # Print tree height and structure after insertion
        print(f"Inserted {key}, Tree Height: {self.calculate_height(self.root)}")
        self.print_tree_structure()
        print("-" * 40)

    def search(self, key):
        node = self._search(self.root, key)
        found = "Found" if node else "Not found"
        print(f"Search for {key}: {found}")
        print(f"Tree Height after search: {self.calculate_height(self.root)}")
        self.print_tree_structure()
        print("-" * 40)
        return node

    def _search(self, node, key):
        if node is None or key == node.key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def minimum(self, node=None):
        if node is None:
            node = self.root
        while node.left is not None:
            node = node.left
        print(f"Minimum key: {node.key}")
        print(f"Tree Height after finding minimum: {self.calculate_height(self.root)}")
        self.print_tree_structure()
        print("-" * 40)
        return node

    def maximum(self, node=None):
        if node is None:
            node = self.root
        while node.right is not None:
            node = node.right
        print(f"Maximum key: {node.key}")
        print(f"Tree Height after finding maximum: {self.calculate_height(self.root)}")
        self.print_tree_structure()
        print("-" * 40)
        return node

    def successor(self, node):
        if node.right is not None:
            succ = self.minimum(node.right)
        else:
            y = node.parent
            while y is not None and node == y.right:
                node = y
                y = y.parent
            succ = y
        succ_key = succ.key if succ else 'None'
        print(f"Successor of {node.key}: {succ_key}")
        print(f"Tree Height after finding successor: {self.calculate_height(self.root)}")
        self.print_tree_structure()
        print("-" * 40)
        return succ

    def predecessor(self, node):
        if node.left is not None:
            pred = self.maximum(node.left)
        else:
            y = node.parent
            while y is not None and node == y.left:
                node = y
                y = y.parent
            pred = y
        pred_key = pred.key if pred else 'None'
        print(f"Predecessor of {node.key}: {pred_key}")
        print(f"Tree Height after finding predecessor: {self.calculate_height(self.root)}")
        self.print_tree_structure()
        print("-" * 40)
        return pred

    def delete(self, key):
        node = self._search(self.root, key)
        if node is None:
            print(f"Key {key} not found.")
            return

        # Case 1: Node has no children
        if node.left is None and node.right is None:
            self._transplant(node, None)
        # Case 2: Node has only one child
        elif node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        # Case 3: Node has two children
        else:
            succ = self.minimum(node.right)
            if succ.parent != node:
                self._transplant(succ, succ.right)
                succ.right = node.right
                succ.right.parent = succ
            self._transplant(node, succ)
            succ.left = node.left
            succ.left.parent = succ

        print(f"Deleted {key}, Tree Height: {self.calculate_height(self.root)}")
        self.print_tree_structure()
        print("-" * 40)

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def in_order_traversal(self, node):
        if node is not None:
            self.in_order_traversal(node.left)
            print(node.key, end=" ")
            self.in_order_traversal(node.right)

    def calculate_height(self, node):
        if node is None:
            return 0
        else:
            left_height = self.calculate_height(node.left)
            right_height = self.calculate_height(node.right)
            return max(left_height, right_height) + 1

    def print_tree_structure(self, node=None, level=0, indent="    "):
        if node is None:
            node = self.root
        if node:
            if level == 0:
                print(node.key)
            if node.left or node.right:
                if node.left:
                    print(indent * level + "├──L: ", end="")
                    print(node.left.key)
                    self.print_tree_structure(node.left, level + 1)
                else:
                    print(indent * level + "├──L: None")
                if node.right:
                    print(indent * level + "└──R: ", end="")
                    print(node.right.key)
                    self.print_tree_structure(node.right, level + 1)
                else:
                    print(indent * level + "└──R: None")

# Testing code
if __name__ == "__main__":
    bst = BST()

    # Insert nodes into the BST
    nodes_to_insert = [50, 30, 70, 20, 40, 60, 80]
    for key in nodes_to_insert:
        bst.insert(key)

    # In-order traversal (sort)
    print("\nIn-order Traversal (Sorted):")
    bst.in_order_traversal(bst.root)
    print("\nTree Height after in-order traversal:", bst.calculate_height(bst.root))
    bst.print_tree_structure()
    print("-" * 40)

    # Search for a key
    bst.search(40)

    # Find minimum and maximum
    bst.minimum()
    bst.maximum()

    # Find successor and predecessor
    node = bst._search(bst.root, 50)
    if node:
        bst.successor(node)
        bst.predecessor(node)

    # Delete nodes
    keys_to_delete = [30, 70, 20]
    for key in keys_to_delete:
        bst.delete(key)
