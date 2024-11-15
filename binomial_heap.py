class BinomialHeapNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None  # Leftmost child
        self.sibling = None  # Right sibling

class BinomialHeap:
    def __init__(self):
        self.head = None

    def make_heap(self):
        return BinomialHeap()

    def insert(self, key):
        """
        Inserts a new key into the binomial heap.

        Args:
          key: The key to be inserted into the heap.

        Returns:
          None

        Side Effects:
          Modifies the heap by adding a new node with the given key.
          Prints the inserted key and the current state of the heap.
        """
        # Create a new node with the given key
        node = BinomialHeapNode(key)
        
        # Create a temporary heap containing only this new node
        temp_heap = self.make_heap()
        temp_heap.head = node
        
        # Merge (union) the temporary heap with the current heap
        self.head = self.union(temp_heap).head
        
        # Print the inserted key
        print(f"Inserted {key}")
        
        # Print the current state of the heap for verification
        self.print_heap()

    def union(self, h2):
        """
        Union two binomial heaps and return the resulting heap.

        This method merges the current binomial heap with another binomial heap (h2)
        and returns a new binomial heap that contains all elements from both heaps.

        Args:
          h2 (BinomialHeap): The binomial heap to be merged with the current heap.

        Returns:
          BinomialHeap: A new binomial heap containing all elements from both heaps.
        """
        # Create a new binomial heap to store the result
        new_heap = self.make_heap()

        # Merge the root lists of the two heaps (sorted by degree)
        new_heap.head = self._merge(self.head, h2.head)

        # If the resulting heap is empty, return it
        if new_heap.head is None:
            return new_heap

        # Initialize pointers for the merge process
        prev = None  # Tracks the previous node
        curr = new_heap.head  # Tracks the current node
        next_node = curr.sibling  # Tracks the next node

        # Traverse through the merged root list to adjust the heap structure
        while next_node:
            # Case 1: Current and next nodes have different degrees
            # Case 2: The next node and its sibling have the same degree (conflict)
            if (curr.degree != next_node.degree) or \
              (next_node.sibling and next_node.sibling.degree == curr.degree):
                prev = curr  # Move prev to curr
                curr = next_node  # Move curr to next
            else:
                # Case 3: Curr and next nodes have the same degree
                if curr.key <= next_node.key:
                    # Curr key is smaller; link next_node as a child of curr
                    curr.sibling = next_node.sibling  # Skip next_node
                    self._link(next_node, curr)  # Link next_node under curr
                else:
                    # Next_node key is smaller; link curr as a child of next_node
                    if prev is None:
                        new_heap.head = next_node  # Update heap head to next_node
                    else:
                        prev.sibling = next_node  # Update prev's sibling to next_node
                    self._link(curr, next_node)  # Link curr under next_node
                    curr = next_node  # Move curr to next_node

            # Move to the next sibling
            next_node = curr.sibling

        # Return the resulting merged heap
        return new_heap

    def _merge(self, h1, h2):
        """
        Merges two binomial trees h1 and h2 into a single binomial tree.

        Args:
          h1 (BinomialNode): The root node of the first binomial tree.
          h2 (BinomialNode): The root node of the second binomial tree.

        Returns:
          BinomialNode: The root node of the merged binomial tree.
        """
         # If one of the lists is empty, return the other
        if h1 is None:
            return h2
        elif h2 is None:
            return h1

        # Initialize the head of the merged list
        if h1.degree <= h2.degree:
            # h1 has the smaller degree, so it becomes the head
            head = h1
            h1 = h1.sibling  # Move to the next node in h1
        else:
            # h2 has the smaller degree, so it becomes the head
            head = h2
            h2 = h2.sibling  # Move to the next node in h2

        # Use 'tail' to keep track of the end of the merged list
        tail = head

        # Traverse both lists until one is exhausted
        while h1 and h2:
            if h1.degree <= h2.degree:
                # h1 has the smaller degree, attach it to the merged list
                tail.sibling = h1
                h1 = h1.sibling  # Move to the next node in h1
            else:
                # h2 has the smaller degree, attach it to the merged list
                tail.sibling = h2
                h2 = h2.sibling  # Move to the next node in h2
            tail = tail.sibling  # Move the tail pointer to the new end of the list

        # Attach the remaining nodes from the non-empty list (if any)
        tail.sibling = h1 if h1 else h2

        # Return the head of the merged list
        return head

    def _link(self, y, z):
        """
        Links two binomial trees by making one tree a child of the other.

        Parameters:
        y (Node): The root of the tree to be linked as a child.
        z (Node): The root of the tree to which y will be linked as a child.

        Returns:
        None
        """
        # Set z as the parent of y
        y.parent = z

        # Attach y as the first child of z.
        # y's sibling pointer is updated to point to the current child of z (if any).
        y.sibling = z.child

        # Update z's child pointer to point to y.
        # This makes y the leftmost child of z.
        z.child = y

        # Increment the degree of z, as it now has one more child.
        z.degree += 1

    def minimum(self):
        """
        Find and return the node with the minimum key in the binomial heap.

        This method traverses the root list of the binomial heap and finds the node
        with the smallest key.

        Returns:
          Node: The node with the minimum key in the binomial heap. If the heap is empty,
              returns None.
        """
        # Initialize y to None. This will hold the node with the minimum key.
        y = None

        # Start traversing the root list from the head of the heap.
        x = self.head

        # Set min_key to a very large value initially to find the smallest key.
        min_key = float('inf')

        # Traverse the root list of binomial trees.
        while x:
            # If the current node's key is smaller than the current minimum,
            # update min_key and y (the node with the smallest key).
            if x.key < min_key:
                min_key = x.key
                y = x

            # Move to the next sibling (next root in the root list).
            x = x.sibling

        # Return the node with the minimum key, or None if the heap is empty.
        return y

    def extract_min(self):
        """
        Extracts the minimum key from the binomial heap and returns it.

        This method finds the root with the minimum key in the binomial heap,
        removes it from the root list, reverses its children, and then merges
        the resulting heap back into the original heap.

        Returns:
          The minimum key in the binomial heap, or None if the heap is empty.
        """
        # If the heap is empty, return None
        if self.head is None:
            return None

        # Initialize variables to find the root with the minimum key
        min_prev = None  # Pointer to the node before the minimum node
        min_node = self.head  # Start by assuming the head is the minimum node
        prev_x = None  # Previous node during traversal
        x = self.head  # Pointer to traverse the root list

        # Traverse the root list to find the node with the smallest key
        while x:
            if x.key < min_node.key:
                # Update the minimum node and its predecessor
                min_node = x
                min_prev = prev_x
            # Move to the next node
            prev_x = x
            x = x.sibling

        # Remove min_node from the root list
        if min_prev:
            # If there is a predecessor, bypass min_node in the sibling chain
            min_prev.sibling = min_node.sibling
        else:
            # If min_node is the head, update the head pointer
            self.head = min_node.sibling

        # Reverse the child list of min_node to prepare for merging back
        child = min_node.child  # Start with the first child of min_node
        new_head = None  # New head for the reversed child list
        while child:
            # Reverse the sibling pointers of the children
            next_child = child.sibling
            child.sibling = new_head
            child.parent = None  # Remove parent reference for new heap
            new_head = child  # Update the new head to the current child
            child = next_child  # Move to the next child

        # Create a new heap for the reversed child list
        new_heap = self.make_heap()
        new_heap.head = new_head

        # Merge the new heap with the current heap
        self.head = self.union(new_heap).head

        # Print and return the minimum key
        print(f"Extracted minimum key {min_node.key}")
        self.print_heap()
        return min_node.key

    def decrease_key(self, x, k):
        """
        Decreases the key of a given node in the binomial heap.

        Parameters:
        x (Node): The node whose key is to be decreased.
        k (int): The new key value. It must be less than or equal to the current key of the node.

        Raises:
        ValueError: If the new key is greater than the current key of the node.

        This method updates the key of the given node to the new key value and then
        ensures the binomial heap property is maintained by moving the node up the
        tree if necessary. The heap is printed after the key is decreased.
        """
        # Check if the new key is valid
        if k > x.key:
            raise ValueError("New key is greater than current key")
        
        # Update the key of the given node
        x.key = k
        
        # Start the bubble-up process to maintain heap property
        y = x  # Current node being evaluated
        z = y.parent  # Parent of the current node

        # While the current node has a parent and violates the heap property
        while z and y.key < z.key:
            # Swap the keys of the current node and its parent
            y.key, z.key = z.key, y.key
            
            # Move up the tree to the parent
            y = z
            z = y.parent

        # Print the heap after decreasing the key
        print(f"Decreased key to {k}")
        self.print_heap()

    def delete(self, x):
        self.decrease_key(x, -float('inf'))
        self.extract_min()

    def find_node(self, key):
        """
        Find a node with the given key in the binomial heap.

        Args:
          key: The key to search for in the binomial heap.

        Returns:
          The node with the specified key if found, otherwise None.
        """
        # Initialize a stack to traverse the heap's root list and subtrees
        stack = [self.head]
        
        # Perform iterative traversal using the stack
        while stack:
            # Pop the top node from the stack
            node = stack.pop()
            
            # Traverse the sibling list starting from the current node
            while node:
                # If the key matches, return the node
                if node.key == key:
                    return node
                
                # If the node has a child, add it to the stack for further traversal
                if node.child:
                    stack.append(node.child)
                
                # Move to the next sibling
                node = node.sibling
        
        # If the key was not found, return None
        return None


    def print_heap(self):
        print("Current Binomial Heap:")
        if not self.head:
            print("Heap is empty")
            return
        self._print_tree(self.head)
        print("-" * 40)

    def _print_tree(self, node, indent=0):
        while node:
            print(' ' * indent + f"Key: {node.key}, Degree: {node.degree}")
            if node.child:
                self._print_tree(node.child, indent + 4)
            node = node.sibling

# Testing the Binomial Heap
if __name__ == "__main__":
    bh = BinomialHeap()

    # Insert keys into the binomial heap
    keys = [27, 11, 8, 17, 14, 38, 6, 29, 12, 18, 1, 25, 10]
    for key in keys:
        bh.insert(key)

    # Print the final heap structure
    print("\nFinal heap structure after all insertions:")
    bh.print_heap()

    # Test minimum function
    min_node = bh.minimum()
    print(f"\nMinimum key in the heap: {min_node.key if min_node else 'Heap is empty'}\n")

    # Test extract_min function
    bh.extract_min()

    # Test decrease_key function
    key_to_decrease = 12
    new_key = 5
    node_to_decrease = bh.find_node(key_to_decrease)
    if node_to_decrease:
        bh.decrease_key(node_to_decrease, new_key)
        print(f"Decreased key {key_to_decrease} to {new_key}\n")

    # Test delete function
    key_to_delete = 25
    node_to_delete = bh.find_node(key_to_delete)
    if node_to_delete:
        bh.delete(node_to_delete)
        print(f"Deleted key {key_to_delete}\n")

    # Test union function
    bh2 = BinomialHeap()
    bh2.insert(3)
    bh2.insert(7)
    print("Second heap after insertions:")
    bh2.print_heap()

    bh.head = bh.union(bh2).head
    print("Heap after union with second heap:")
    bh.print_heap()