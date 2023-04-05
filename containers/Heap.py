'''
This file implements the Heap data structure as a subclass of the BinaryTree.
The book implements Heaps using an *implicit* tree with an *explicit* vector implementation,
so the code in the book is likely to be less helpful than the code for the other data structures.
The book's implementation is the traditional implementation because it has a faster constant factor
(but the same asymptotics).
This homework is using an explicit tree implementation to help you get more practice with OOP-style programming and classes.
'''

from containers.BinaryTree import BinaryTree, Node


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        self.root = None
        self.size = 0
        super().__init__()
        if xs is not None:
            # this assumes that xs is always a list
            for element in xs:
                self.insert(element)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            print(self.root)
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        ret = True
        if node is None:
            return True
        leftHeap = Heap._is_heap_satisfied(node.left)
        rightHeap = Heap._is_heap_satisfied(node.right)
        if not leftHeap or not rightHeap:
            ret = False
        if node.left is not None and node.left.value < node.value:
            ret = False
        if node.right is not None and node.right.value < node.value:
            ret = False
        # ensure left to right property
        lastLevel = [node]
        leaf = False
        while not leaf:
            nextLevel = []
            for n in lastLevel:
                if n.left is not None:
                    nextLevel.append(n.left)
                if n.right is not None:
                    nextLevel.append(n.right)
                if n.left is None or n.right is None:
                    leaf = True
            if len(nextLevel) == 0 and not leaf:
                ret = False
            for i in range(len(nextLevel) - 1):
                if nextLevel[i+1].left is None and nextLevel[i+1].right is not None:
                    ret = False
            lastLevel = nextLevel
        return ret

    def insert(self, value):
        '''
        Inserts value into the heap.

        FIXME:
        Implement this function.

        HINT:
        The pseudo code is
        1. Find the next position in the tree using the binary representation of the total number of nodes
            1. You will have to explicitly store the size of your heap in a variable (rather than compute it) to maintain the O(log n) runtime
            1. See https://stackoverflow.com/questions/18241192/implement-heap-using-a-binary-tree for hints
        1. Add `value` into the next position
        1. Recursively swap value with its parent until the heap property is satisfied

        HINT:
        Create a @staticmethod helper function,
        following the same pattern used in the BST and AVLTree insert functions.
        '''
        if not self.root:
            self.root = Node(value)
            return self.root
        # find insert position
        binary_str = bin(self.size+1)[3:]
        # Convert heap size to binary and ignore most significant bit
        curr_node = self.root
        # Start at the root node
        for bit in binary_str:
            if bit == '1':
                if curr_node.right is not None:
                    curr_node = curr_node.right
                elif curr_node.left is not None:
                    curr_node = curr_node.left
                else:
                    # Last level is not full, return leftmost node in last level
                    curr_node = self.root
                    while curr_node.left is not None:
                        curr_node = curr_node.left
                    break
            else:
                if curr_node.left is not None:
                    curr_node = curr_node.left
                elif curr_node.right is not None:
                    curr_node = curr_node.right
                else:
                    break
        # if (curr_node is not None and curr_node.parent is not None):
        # curr_node = curr_node.parent
        self.size += 1

        node = None
        if curr_node.left is None:
            curr_node.left = Node(value)
            curr_node.left.parent = curr_node
            node = curr_node.left
        else:
            curr_node.right = Node(value)
            curr_node.right.parent = curr_node
            node = curr_node.right
        
        # bubble up
        while node is not None and node.parent is not None and node != node.parent and node.value < node.parent.value:
            node.value, node.parent.value = node.parent.value, node.value
            node = node.parent

    def check_for_swap(self, curr_node):
        if not curr_node:
            return
        if (curr_node.left and curr_node.left.value < curr_node.value):
            temp = curr_node.left.value
            curr_node.left.value = curr_node.value
            curr_node.value = temp
        if (curr_node.right and curr_node.right.value < curr_node.value):
            temp = curr_node.right.value
            curr_node.right.value = curr_node.value
            curr_node.value = temp

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for elt in xs:
            self.insert(elt)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        return self.root.value

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        The pseudocode is
        1. remove the bottom right node from the tree
        2. replace the root node with what was formerly the bottom right
        3. "trickle down" the root node: recursively swap it with its largest child until the heap property is satisfied

        HINT:
        I created two @staticmethod helper functions: _remove_bottom_right and _trickle.
        It's possible to do it with only a single helper (or no helper at all),
        but I personally found dividing up the code into two made the most sense.
        '''
        if self.root:
            # find bottom right node
            queue = [self.root]
            curr = None
            while queue:
                level_size = len(queue)
                for i in range(level_size):
                    curr = queue.pop(0)
                    if curr.left is not None:
                        queue.append(curr.left)
                    if curr.right is not None:
                        queue.append(curr.right)
            # at this point, curr = bottom right most
            value = curr.value
            if curr.parent is None:
                # removing root
                self.root = None
                return
            if curr.parent.right is None:
                curr.parent.left = None
            else:
                curr.parent.right = None
            self.root.value = value
            # now bubble down
            curr = self.root
            while curr.left is not None or curr.right is not None:
                # Determine the index of the smallest child
                smallest_child = None
                if curr.left is not None and curr.right is not None:
                    if curr.left.value < curr.right.value:
                        smallest_child = curr.left
                    else:
                        smallest_child = curr.right
                elif curr.left is not None:
                    smallest_child = curr.left
                elif curr.right is not None:
                    smallest_child = curr.right
                # Swap with smallest child if necessary
                # and continue bubbling down
                if smallest_child is not None and smallest_child.value < curr.value:
                    curr.value, smallest_child.value = smallest_child.value, curr.value
                    curr = smallest_child
                else:
                    break
