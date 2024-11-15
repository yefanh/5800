import re
import numpy as np
import matplotlib.pyplot as plt

class Node:
    """Node class for linked list in hash table collision management."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    """Hash table using linked lists for collision handling."""
    
    def __init__(self, m=30):
        self.m = m  # Number of slots in the hash table
        self.table = [None] * m  # Initialize table with None

    def _hash(self, key):
        """Improved hash function using polynomial rolling."""
        p = 31  # A small prime number
        m = self.m
        hash_value = 0
        p_pow = 1

        for char in key:
            hash_value = (hash_value + (ord(char) - ord('a') + 1) * p_pow) % m
            p_pow = (p_pow * p) % m

        return hash_value

    def insert(self, key, value):
        """Insert a key-value pair into the hash table."""
        index = self._hash(key)
        head = self.table[index]
        
        # Check if key already exists in the list
        current = head
        while current is not None:
            if current.key == key:
                current.value = value  # Update value if key is found
                return
            current = current.next
        
        # Insert new node at the beginning of the list
        new_node = Node(key, value)
        new_node.next = head
        self.table[index] = new_node

    def delete(self, key):
        """Delete a key-value pair from the hash table."""
        index = self._hash(key)
        current = self.table[index]
        prev = None
        
        while current is not None:
            if current.key == key:
                if prev is None:
                    # Remove head node
                    self.table[index] = current.next
                else:
                    # Remove non-head node
                    prev.next = current.next
                return
            prev = current
            current = current.next
        print(f"Key {key} not found for deletion.")

    def increase(self, key):
        """Increase the value associated with the key by 1."""
        index = self._hash(key)
        current = self.table[index]
        
        while current is not None:
            if current.key == key:
                current.value += 1
                return
            current = current.next

        # If key doesn't exist, insert it with value 1
        self.insert(key, 1)

    def find(self, key):
        """Find the value associated with the key."""
        index = self._hash(key)
        current = self.table[index]
        
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def list_all_keys(self):
        """List all keys and their counts."""
        result = []
        for head in self.table:
            current = head
            while current is not None:
                result.append((current.key, current.value))
                current = current.next
        return result

def process_text(text, hash_table):
    """Process the text to insert word counts into the hash table."""
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        hash_table.increase(word)


def save_output(hash_table, filename="output.txt"):
    """Save the list of words and their counts to a file."""
    with open(filename, "w") as f:
        for key, value in hash_table.list_all_keys():
            f.write(f"{key}: {value}\n")


def analyze_collisions(hash_table):
    """Analyze collision lengths and calculate variance, displaying a histogram."""
    # Collect lengths of linked lists at each slot
    lengths = np.zeros(hash_table.m, dtype=int)
    for i in range(hash_table.m):
        current = hash_table.table[i]
        while current is not None:
            lengths[i] += 1
            current = current.next

    # Calculate variance using numpy for efficiency
    variance = np.var(lengths)

    # Plot histogram of collision list lengths
    plt.figure(figsize=(10, 6))
    plt.hist(lengths, bins=range(0, max(lengths)+2), edgecolor="black", align="left")
    plt.xlabel("Length of Collision Lists")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Collision List Lengths (m={hash_table.m})")
    plt.show()

    # Calculate the longest 10% of lists
    sorted_lengths = np.sort(lengths)[::-1]
    num_longest = max(1, len(sorted_lengths) // 10)
    longest_10_percent = sorted_lengths[:num_longest]

    return {
        "variance": variance,
        "histogram_data": lengths,
        "longest_10_percent": longest_10_percent
    }


# Test with different values of m
if __name__ == "__main__":
    for m in [30, 300, 1000]:
        print(f"\nTesting with m = {m}")
        hash_table = HashTable(m=m)

        # Load the sample text
        with open("alice_in_wonderland.txt", "r", encoding="latin-1") as file:
            text = file.read()

        # Process the text and populate the hash table
        process_text(text, hash_table)

        # Test specific operations after populating the hash table
        # 1. Insert a new key-value pair
        hash_table.insert("new_word", 10)
        print(f"Inserted ('new_word', 10). Find 'new_word':", hash_table.find("new_word"))

        # 2. Increase the count of an existing key
        hash_table.increase("alice")
        print(f"Increased count for 'alice'. Find 'alice':", hash_table.find("alice"))

        # 3. Delete an existing key
        hash_table.delete("rabbit")
        print("Deleted 'rabbit'. Find 'rabbit':", hash_table.find("rabbit"))

        # 4. List all keys and their counts (this will be limited to a few examples for readability)
        all_keys = hash_table.list_all_keys()
        print("Sample of all keys and their counts:", all_keys[:10])  # Print the first 10 for brevity

        # Save the output to a file
        save_output(hash_table, filename=f"word_counts_m_{m}.txt")

        # Analyze collisions and display the histogram
        analysis = analyze_collisions(hash_table)
        print(f"Variance in list lengths for m = {m}: {analysis['variance']}")
        print(f"Longest 10% of lists for m = {m}: {analysis['longest_10_percent']}")
