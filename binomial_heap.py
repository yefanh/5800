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
        node = BinomialHeapNode(key)
        temp_heap = self.make_heap()
        temp_heap.head = node
        self.head = self.union(temp_heap).head
        print(f"Inserted {key}")
        self.print_heap()

    def union(self, h2):
        new_heap = self.make_heap()
        new_heap.head = self._merge(self.head, h2.head)
        if new_heap.head is None:
            return new_heap

        prev = None
        curr = new_heap.head
        next_node = curr.sibling

        while next_node:
            if (curr.degree != next_node.degree) or \
               (next_node.sibling and next_node.sibling.degree == curr.degree):
                prev = curr
                curr = next_node
            else:
                if curr.key <= next_node.key:
                    curr.sibling = next_node.sibling
                    self._link(next_node, curr)
                else:
                    if prev is None:
                        new_heap.head = next_node
                    else:
                        prev.sibling = next_node
                    self._link(curr, next_node)
                    curr = next_node
            next_node = curr.sibling
        return new_heap

    def _merge(self, h1, h2):
        if h1 is None:
            return h2
        elif h2 is None:
            return h1
        else:
            if h1.degree <= h2.degree:
                head = h1
                h1 = h1.sibling
            else:
                head = h2
                h2 = h2.sibling
            tail = head

            while h1 and h2:
                if h1.degree <= h2.degree:
                    tail.sibling = h1
                    h1 = h1.sibling
                else:
                    tail.sibling = h2
                    h2 = h2.sibling
                tail = tail.sibling

            tail.sibling = h1 if h1 else h2
            return head

    def _link(self, y, z):
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def minimum(self):
        y = None
        x = self.head
        min_key = float('inf')
        while x:
            if x.key < min_key:
                min_key = x.key
                y = x
            x = x.sibling
        return y

    def extract_min(self):
        if self.head is None:
            return None

        # Find the root with minimum key
        min_prev = None
        min_node = self.head
        prev_x = None
        x = self.head
        while x:
            if x.key < min_node.key:
                min_node = x
                min_prev = prev_x
            prev_x = x
            x = x.sibling

        # Remove min_node from root list
        if min_prev:
            min_prev.sibling = min_node.sibling
        else:
            self.head = min_node.sibling

        # Reverse min_node's children and make new heap
        child = min_node.child
        new_head = None
        while child:
            next_child = child.sibling
            child.sibling = new_head
            child.parent = None
            new_head = child
            child = next_child

        new_heap = self.make_heap()
        new_heap.head = new_head
        self.head = self.union(new_heap).head

        print(f"Extracted minimum key {min_node.key}")
        self.print_heap()
        return min_node.key

    def decrease_key(self, x, k):
        if k > x.key:
            raise ValueError("New key is greater than current key")
        x.key = k
        y = x
        z = y.parent

        while z and y.key < z.key:
            y.key, z.key = z.key, y.key
            y = z
            z = y.parent
        print(f"Decreased key to {k}")
        self.print_heap()

    def delete(self, x):
        self.decrease_key(x, -float('inf'))
        self.extract_min()

    def find_node(self, key):
        stack = [self.head]
        while stack:
            node = stack.pop()
            while node:
                if node.key == key:
                    return node
                if node.child:
                    stack.append(node.child)
                node = node.sibling
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