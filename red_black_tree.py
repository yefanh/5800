class Node:
    def __init__(self, key, color="RED", left=None, right=None, parent=None):
        self.key = key
        self.color = color  # "RED" or "BLACK"
        self.left = left
        self.right = right
        self.parent = parent


class RedBlackTree:
    def __init__(self):
        self.T_nil = Node(key=None, color="BLACK")  # Sentinel node
        self.root = self.T_nil

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.T_nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.T_nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.T_nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.T_nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def print_tree_structure(self, node=None, level=0, indent="    "):
        if node is None:
            node = self.root
        if node != self.T_nil:
            if level == 0:
                print(f"{(node.key, node.color)}")
            if node.left != self.T_nil or node.right != self.T_nil:
                if node.left != self.T_nil:
                    print(indent * level + "├──", end="")
                    print(f"L: {(node.left.key, node.left.color)}")
                    self.print_tree_structure(node.left, level + 1)
                else:
                    print(indent * level + "├──L: None")
                if node.right != self.T_nil:
                    print(indent * level + "└──", end="")
                    print(f"R: {(node.right.key, node.right.color)}")
                    self.print_tree_structure(node.right, level + 1)
                else:
                    print(indent * level + "└──R: None")

    def insert(self, key):
        new_node = Node(key=key, left=self.T_nil, right=self.T_nil, parent=None)
        y = self.T_nil
        x = self.root
        while x != self.T_nil:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        new_node.parent = y
        if y == self.T_nil:
            self.root = new_node  # Tree was empty
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node
        new_node.left = self.T_nil
        new_node.right = self.T_nil
        new_node.color = "RED"
        self.insert_fixup(new_node)
        # After insertion, print the height and tree structure
        print(f"Inserted {key}, Tree Height: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)

    def insert_fixup(self, z):
        while z.parent and z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.left_rotate(z.parent.parent)
        self.root.color = "BLACK"

    def search(self, key):
        current = self.root
        while current != self.T_nil and key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        # After search, print the height and tree structure
        print(f"Searching for {key}: {'Found' if current != self.T_nil else 'Not found'}")
        print(f"Tree Height after search: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)
        return current if current != self.T_nil else None

    def minimum(self, node=None):
        if node is None:
            node = self.root
        while node.left != self.T_nil:
            node = node.left
        # After finding minimum, print the height and tree structure
        print(f"Minimum key: {node.key}")
        print(f"Tree Height after finding minimum: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)
        return node

    def maximum(self, node=None):
        if node is None:
            node = self.root
        while node.right != self.T_nil:
            node = node.right
        # After finding maximum, print the height and tree structure
        print(f"Maximum key: {node.key}")
        print(f"Tree Height after finding maximum: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)
        return node

    def successor(self, x):
        if x.right != self.T_nil:
            succ = self.minimum(x.right)
        else:
            y = x.parent
            while y != self.T_nil and x == y.right:
                x = y
                y = y.parent
            succ = y
        # After finding successor, print the height and tree structure
        print(f"Successor of {x.key}: {succ.key if succ else 'None'}")
        print(f"Tree Height after finding successor: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)
        return succ

    def predecessor(self, x):
        if x.left != self.T_nil:
            pred = self.maximum(x.left)
        else:
            y = x.parent
            while y != self.T_nil and x == y.left:
                x = y
                y = y.parent
            pred = y
        # After finding predecessor, print the height and tree structure
        print(f"Predecessor of {x.key}: {pred.key if pred else 'None'}")
        print(f"Tree Height after finding predecessor: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)
        return pred

    def in_order_traversal(self, node=None):
        if node is None:
            node = self.root
        if node != self.T_nil:
            self.in_order_traversal(node.left)
            print(node.key, end=" ")
            self.in_order_traversal(node.right)

    def print_tree(self):
        self.in_order_traversal()
        print()

    def calculate_height(self, node=None):
        if node is None:
            node = self.root
        if node == self.T_nil:
            return 0
        left_height = self.calculate_height(node.left)
        right_height = self.calculate_height(node.right)
        return max(left_height, right_height) + 1

    # Placeholder for delete method
    def delete(self, key):
        pass  # Delete method not implemented here


# Sample usage
rb_tree = RedBlackTree()
# Sample operations
nodes_to_insert = [30, 15, 70, 10, 20, 60, 85, 5, 50, 65, 80, 90, 40, 55]
for key in nodes_to_insert:
    rb_tree.insert(key)

# Testing in-order traversal (sort)
print("\nIn-order traversal (sorted keys):")
rb_tree.in_order_traversal()
print()
print(f"Tree Height after in-order traversal: {rb_tree.calculate_height()}")
rb_tree.print_tree_structure()
print("-" * 40)

# Testing search
rb_tree.search(60)

# Testing minimum
rb_tree.minimum()

# Testing maximum
rb_tree.maximum()

# Testing successor
node = rb_tree.search(55)
if node:
    rb_tree.successor(node)

# Testing predecessor
if node:
    rb_tree.predecessor(node)

# Note: The delete operation is not implemented. If you implement it, you can add similar print statements after deletion.