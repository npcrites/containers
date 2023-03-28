'''
This file implements the Binary Search Tree data structure.
The functions in this file are considerably harder than the
functions in the BinaryTree file.
'''

from containers.BinaryTree import BinaryTree, Node


class BST(BinaryTree):
    '''
    The BST is a superclass of BinaryTree.
    That means that the BST class "inherits" all of
    the methods from BinaryTree,
    and we don't have to reimplement them.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the BST.
        '''
        super().__init__()
        self.root = None
        if xs is not None:
            for element in xs:
                self.insert(element)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can
        be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command BST([1,2,3])
        it's __repr__ will return "BST([1,2,3])"
        For the BST, type(self).__name__ will be the string "BST",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of BST will have
        a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_bst_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function
        that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether
        insert/delete functions
        are actually working.
        '''
        if self.root:
            return BST._is_bst_satisfied(self.root)
        return True

    @staticmethod
    def _is_bst_satisfied(node):
        '''
        FIXME:
        The current implementation has a bug:
        it only checks if the children of the current
        node are less than/greater than,
        rather than ensuring that all nodes to the
        left/right are less than/greater than.
        HINT:
        Use the _find_smallest and _find_largest functions to fix the bug.
        You should use the _ prefixed methods because
        those are static methods just like this one.
        '''
        ret = True
        if node.left:
            if node.value >= node.left.value:
                ret &= BST._is_bst_satisfied(node.left)
                if BST._find_largest(node.left) > node.value:
                    ret = False
            else:
                ret = False
        if node.right:
            if node.value <= node.right.value:
                ret &= BST._is_bst_satisfied(node.right)
                if BST._find_smallest(node.right) < node.value:
                    ret = False
            else:
                ret = False
        return ret

    def insert(self, value):
        '''
        Inserts value into the BST.
        FIXME:
        Implement this function.
        HINT:
        Create a staticmethod helper function following
        the pattern of _is_bst_satisfied.
        '''
        if self.root is None:
            self.root = Node(value)
        else:
            BST._insert(self.root, value)

    @staticmethod
    def _insert(node, value):
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = BST._insert(node.left, value)
        else:
            node.right = BST._insert(node.right, value)
        return node

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.
        FIXME:
        Implement this function.
        HINT:
        Repeatedly call the insert method.
        You cannot get this method to work correctly
        until you have gotten insert to work correctly.
        '''
        for element in xs:
            self.insert(element)

    def __contains__(self, value):
        '''
        Recall that `x in tree` desugars to `tree.__contains__(x)`.
        '''
        return self.find(value)

    def find(self, value):
        '''
        Returns whether value is contained in the BST.
        FIXME:
        Implement this function.
        '''
        return BST._find(value, self.root)

    @staticmethod
    def _find(value, node):
        '''
        FIXME:
        Implement this function.
        '''
        if node is None:
            return False
        if node.value == value:
            return True
        if node.value > value:
            return BST._find(value, node.left)
        else:
            return BST._find(value, node.right)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_smallest(self.root)

    @staticmethod
    def _find_smallest(node):
        '''
        This is a helper function for find_smallest and
        not intended to be called directly by the user.
        '''
        assert node is not None
        if node.left is None:
            return node.value
        else:
            return BST._find_smallest(node.left)

    def find_largest(self):
        '''
        Returns the largest value in the tree.
        FIXME:
        Implement this function.
        HINT:
        Follow the pattern of the _find_smallest function.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_largest(self.root)

    @staticmethod
    def _find_largest(node):
        assert node is not None
        if node.right is None:
            return node.value
        else:
            return BST._find_largest(node.right)

    def remove(self, value):
        '''
        Removes value from the BST.
        If value is not in the BST, it does nothing.
        FIXME:
        Implement this function.
        HINT:
        You should have everything else working
        before you implement this function.
        HINT:
        Use a recursive helper function.
        '''
        if self.root is not None:
            if value == self.root.value:
                if self.root.left is None:
                    if self.root.right is None:
                        self.root = None
        else:
            BST._remove(value, self.root)
        print("post deleting " + str(value))
        print(self.root)

    @staticmethod
    def _remove(value, node):
        if node is None:
            return node
        if value < node.value:
            node.left = BST._remove(value, node.left)
        elif value > node.value:
            node.right = BST._remove(value, node.right)
        else:
            # node with one child or none
            if node.left is None and node.right is None:
                node = None
                return node
            elif node.left is None:
                temp = node.right
                node.value = node.right.value
                node.right = node.right.right
                # node.right = None
                return temp
            elif node.right is None:
                temp = node.left
                node.value = node.left.value
                node.left = node.left.left
                # node.left = None
                return temp
            # node with two children, largest right sbt successor
            else:
                temp = BST._find_smallest(node.right)
                node.value = temp
                node.right = BST._remove(temp, node.right)
        return node

    def remove_list(self, xs):
        '''
        Given a list xs, remove each element of xs from self.
        FIXME:
        Implement this function.
        HINT:
        See the insert_list function.
        '''
        for element in xs:
            self.remove(element)

    def __iter__(self):
        return BSTIter(self.inorder(self.root, ""))


class BSTIter:
    def __init__(self, xs):
        self.xs = xs
        self.i = 0

    def __next__(self):
        if self.i >= len(self.xs):
            raise StopIteration
        else:
            result = self.xs[self.i]
            self.i += 1
            return
