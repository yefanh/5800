import random

class Node:
    def __init__(self, key, level):
        self.key = key
        # Forward references for each level
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        """
        Initialize a skip list.
        :param max_level: Maximum level for the skip list (default is 16).
        :param p: Probability for determining the level of each new node (default is 0.5).
        """
        self.MAX_LEVEL = max_level  # The maximum number of levels allowed in the skip list.
        self.P = p  # Probability used to determine the height of nodes.
        # Create the header node with the maximum number of levels and a key of negative infinity.
        self.header = self.create_node(self.MAX_LEVEL, -float('inf'))
        self.level = 0  # Tracks the current highest level in the skip list.

    def create_node(self, lvl, key):
        """
        Create a new node for the skip list.
        :param lvl: Number of levels this node spans.
        :param key: The key stored in the node.
        :return: A new node with the given key and level.
        """
        return Node(key, lvl)  # Create a Node object with the given key and level.

    def random_level(self):
        """
        Generate a random level for a new node based on the probability `P`.
        :return: A random level (integer) between 0 and MAX_LEVEL.
        """
        lvl = 0  # Start at level 0.
        # Increment the level with probability `P` until the maximum level is reached.
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl  # Return the generated random level.

    def insert(self, key):
      # Step 1: Initialize a list to track nodes that need their forward pointers updated
      update = [None] * (self.MAX_LEVEL + 1)
      current = self.header  # Start traversal from the header node

      # Step 2: Traverse the skip list from the highest level down to level 0
      for i in reversed(range(self.level + 1)):  # Start from the highest level and go down
          # Move forward in the current level until the key is smaller than the next node's key
          while current.forward[i] and current.forward[i].key < key:
              current = current.forward[i]  # Move forward on the same level
          update[i] = current  # Save the node where the traversal stopped at this level

      # Step 3: Move to level 0 to check if the key already exists
      current = current.forward[0]  # Move one step forward at level 0

      # Step 4: If the key is not present, insert it
      if current is None or current.key != key:
          # Generate a random level for the new node
          rlevel = self.random_level()

          # Step 5: If the new node's level is higher than the current skip list level,
          # initialize `update` pointers for the new levels and update the skip list level
          if rlevel > self.level:
              for i in range(self.level + 1, rlevel + 1):
                  update[i] = self.header  # At higher levels, the header node will point to the new node
              self.level = rlevel  # Update the skip list's current maximum level

          # Step 6: Create a new node with the random level and key
          n = self.create_node(rlevel, key)

          # Step 7: Update forward pointers in all levels for the new node
          for i in range(rlevel + 1):  # Loop through all levels up to the new node's level
              n.forward[i] = update[i].forward[i]  # Point the new node to the next node
              update[i].forward[i] = n  # Update the previous node to point to the new node

          # Step 8: Print a message indicating successful insertion and the updated structure
          print(f"Inserted {key}")
          self.print_structure()  # Visualize the updated skip list structure

      # Step 9: If the key already exists, print a message
      else:
          print(f"Key {key} already exists")


    def delete(self, key):
      # Initialize an update list to track nodes that need their forward pointers updated
      update = [None] * (self.MAX_LEVEL + 1)
      
      # Start from the header node of the skip list
      current = self.header

      # Traverse the skip list from the highest level down to level 0
      # The goal is to find the position where the node with the target key might exist
      for i in reversed(range(self.level + 1)):  # Start from the highest level and go down
          # Move forward in the current level until the key is larger than the current node's key
          while current.forward[i] and current.forward[i].key < key:
              current = current.forward[i]
          # Save the current node in the update list for the current level
          update[i] = current

      # Move to level 0 to check if the key actually exists in the skip list
      current = current.forward[0]

      # If the key is found in the skip list
      if current and current.key == key:
          # Update forward pointers for all levels where the node exists
          for i in range(self.level + 1):  # Traverse all levels from 0 to the current highest level
              # If the forward pointer at this level points to the node being deleted, update it
              if update[i].forward[i] != current:
                  continue
              update[i].forward[i] = current.forward[i]

          # Adjust the level of the skip list
          # If the highest levels have no nodes, reduce the level of the skip list
          while self.level > 0 and self.header.forward[self.level] is None:
              self.level -= 1

          # Print confirmation of deletion and the updated skip list structure
          print(f"Deleted {key}")
          self.print_structure()

      # If the key is not found, print an appropriate message
      else:
          print(f"Key {key} not found")


    def search(self, key):
      # Start from the header node
      current = self.header
      print(f"Searching for {key}:")  # Print the key being searched for

      # Step 1: Traverse the skip list from the highest level to level 0
      for i in reversed(range(self.level + 1)):  # Start from the highest level and go down
          # Step 2: Move forward in the current level while the next node's key is smaller than the target key
          while current.forward[i] and current.forward[i].key < key:
              # Print the move to the right, showing the current key and the key of the next node
              print(f"At level {i}, moving right from {current.key} to {current.forward[i].key}")
              current = current.forward[i]  # Move forward to the next node
          # Print the move down to the next level
          print(f"At level {i}, moving down")

      # Step 3: Move to the next node at level 0 to check if the key exists
      current = current.forward[0]

      # Step 4: Check if the current node's key matches the target key
      if current and current.key == key:
          print(f"Found key {key}")  # Print success message if key is found
          return True  # Return True to indicate the key is found

      # Step 5: If the key is not found, print a failure message
      print(f"Key {key} not found")
      return False  # Return False to indicate the key is not found


    def print_structure(self):
      # Print a header to indicate the skip list structure is being displayed
      print("Skiplist structure:")

      # Step 1: Traverse each level of the skip list, starting from the highest level
      for i in reversed(range(self.level + 1)):  # Start from the highest level and go down
          current = self.header.forward[i]  # Begin at the first node of the current level

          # Print the current level label
          print(f"Level {i}: ", end="")

          # Step 2: Print all nodes in the current level
          while current:
              print(current.key, end=" ")  # Print the key of each node on this level
              current = current.forward[i]  # Move to the next node on the same level

          # Move to the next line after finishing the current level
          print("")

      # Step 3: Print a separator line for better visualization
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
        #("delete", 20),
        ("insert", 100),
        ("insert", 20),
        ("insert", 30),
        #("delete", 5),
        ("insert", 50),
        #("search", 80),

        ("insert", 10),
        ("insert", 10),
        ("search", 200)
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
