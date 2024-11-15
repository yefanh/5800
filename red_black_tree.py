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
        """
        Performs a left rotation on node x.
        """
        y = x.right
        x.right = y.left
        if y.left != self.T_nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.T_nil or x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        """
        Performs a right rotation on node x.
        """
        y = x.left
        x.left = y.right
        if y.right != self.T_nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.T_nil or x.parent is None:
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
        """
        Inserts a new node with the given key into the Red-Black Tree.
        """
        new_node = Node(key=key, left=self.T_nil, right=self.T_nil)
        y = self.T_nil
        x = self.root

        # Find the correct position for the new node
        while x != self.T_nil:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        new_node.parent = y

        # Insert the new node
        if y == self.T_nil:
            self.root = new_node  # Tree was empty
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node

        # Initialize the new node's properties
        new_node.left = self.T_nil
        new_node.right = self.T_nil
        new_node.color = "RED"

        # Fix the Red-Black Tree properties
        self.insert_fixup(new_node)

        # After insertion, print the height and tree structure
        print(f"Inserted {key}, Tree Height: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)

    def insert_fixup(self, z):
        """
        Fixes the Red-Black Tree after insertion to maintain properties.
        """
        while z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # Uncle
                if y.color == "RED":
                    # Case 1: Uncle is red
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # Case 2: z is right child
                        z = z.parent
                        self.left_rotate(z)
                    # Case 3: z is left child
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left  # Uncle
                if y.color == "RED":
                    # Case 1: Uncle is red
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        # Case 2: z is left child
                        z = z.parent
                        self.right_rotate(z)
                    # Case 3: z is right child
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
        print(f"Successor of {x.key}: {succ.key if succ != self.T_nil else 'None'}")
        print(f"Tree Height after finding successor: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)
        return succ if succ != self.T_nil else None

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
        print(f"Predecessor of {x.key}: {pred.key if pred != self.T_nil else 'None'}")
        print(f"Tree Height after finding predecessor: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)
        return pred if pred != self.T_nil else None

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

    def delete(self, key):
        z = self.search(key)
        if z is None:
            print(f"Key {key} not found in the tree.")
            return
        self.delete_node(z)
        # After deletion, print the height and tree structure
        print(f"Deleted {key}, Tree Height: {self.calculate_height()}")
        self.print_tree_structure()
        print("-" * 40)

    def delete_node(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.T_nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.T_nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "BLACK":
            self.delete_fixup(x)

    def transplant(self, u, v):
        if u.parent == self.T_nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_fixup(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"

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

# Testing delete
keys_to_delete = [70, 15, 5]
for key in keys_to_delete:
    rb_tree.delete(key)


# Sample usage with specific insertions to trigger all cases
rb_tree1 = RedBlackTree()
# Insert nodes to trigger Case 1
rb_tree1.insert(10)
rb_tree1.insert(5)
rb_tree1.insert(15)
rb_tree1.insert(1)  # Triggers Case 1

# Insert nodes to trigger Case 2
rb_tree1.insert(7)  # Triggers Case 2

# Insert nodes to trigger Case 3
rb_tree1.insert(6)  # Triggers Case 3