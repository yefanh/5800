import random

class Node:
    def __init__(self, key, level):
        self.key = key
        # Forward references for each level
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.MAX_LEVEL = max_level
        self.P = p  # Probability for random level generation
        self.header = self.create_node(self.MAX_LEVEL, -float('inf'))
        self.level = 0

    def create_node(self, lvl, key):
        return Node(key, lvl)

    def random_level(self):
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        # Start from highest level of skip list
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        # Move to level 0
        current = current.forward[0]

        # If current is None or key is not present, insert key
        if current is None or current.key != key:
            rlevel = self.random_level()

            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            n = self.create_node(rlevel, key)
            for i in range(rlevel + 1):
                n.forward[i] = update[i].forward[i]
                update[i].forward[i] = n
            print(f"Inserted {key}")
            self.print_structure()
        else:
            print(f"Key {key} already exists")

    def delete(self, key):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    continue
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            print(f"Deleted {key}")
            self.print_structure()
        else:
            print(f"Key {key} not found")

    def search(self, key):
        current = self.header
        print(f"Searching for {key}:")
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key < key:
                print(f"At level {i}, moving right from {current.key} to {current.forward[i].key}")
                current = current.forward[i]
            print(f"At level {i}, moving down")
        current = current.forward[0]
        if current and current.key == key:
            print(f"Found key {key}")
            return True
        print(f"Key {key} not found")
        return False

    def print_structure(self):
        print("Skiplist structure:")
        for i in reversed(range(self.level + 1)):
            current = self.header.forward[i]
            print(f"Level {i}: ", end="")
            while current:
                print(current.key, end=" ")
                current = current.forward[i]
            print("")
        print("-" * 40)

# Example usage
if __name__ == "__main__":
    skip_list = SkipList(max_level=50)

    operations = [
        ("insert", 20),
        ("insert", 40),
        ("insert", 10),
        ("insert", 20),
        ("insert", 5),
        ("insert", 80),
        ("delete", 20),
        ("insert", 100),
        ("insert", 20),
        ("insert", 30),
        ("delete", 5),
        ("insert", 50),
        ("search", 80),
    ]

    for op, value in operations:
        if op == "insert":
            skip_list.insert(value)
        elif op == "delete":
            skip_list.delete(value)
        elif op == "search":
            skip_list.search(value)
        else:
            print(f"Unknown operation {op}")
