'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder
than the functions in the BinaryTree and BST files,
but there are fewer of them.
'''

from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST
import copy


class AVLTree(BST):

    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the
    class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()
        # what about xs?
        self.root = None
        if xs is not None:
            if (type(xs) == int):
                self.root = Node(xs)
            else:
                for elt in xs:
                    AVLTree._insert(self.root, elt)

    def __eq__(self, other):
        if self.root is None:
            return other.root is None
        else:
            return self.root.value == other.root.value and self.root.left.__eq__(other.left) and self.root.right.__eq__(other.right)

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returns the balance factor of a node.
        '''
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)

    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all
        nodes have a balance factor in [-1,0,1].
        '''
        return AVLTree._is_avl_satisfied(self.root)

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        print("is avl satisfied:")
        print(node)
        if not node:
            return True
        # balance_factor = AVLTree._balance_factor(node)
        return (
            abs(AVLTree._balance_factor(node)) <= 1
            and AVLTree._is_avl_satisfied(node.left)
            and AVLTree._is_avl_satisfied(node.right)
        )

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree
        code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        node1 = copy.deepcopy(node)
        new_root = copy.deepcopy(node1.right)
        node1.right = new_root.left
        if new_root.left is not None:
            new_root.left.parent = node1
        new_root.left = node1
        node1.parent = new_root
        return new_root

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code
        is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        node1 = copy.deepcopy(node)
        new_root = copy.deepcopy(node1.left)
        node1.left = new_root.right
        if new_root.right is not None:
            new_root.right.parent = node1
        new_root.right = node1
        node1.parent = new_root

        return new_root

    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of how
        to insert into an AVL tree,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree
        code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to
        the code for your insert function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        if not self.root:
            self.root = Node(value)
        else:
            self.root = self._insert(self.root, value)

    @staticmethod
    def _insert(node, value):
        if not node:
            return Node(value)
            # is this a redundant step?
        if value < node.value:
            node.left = AVLTree._insert(node.left, value)
        else:
            node.right = AVLTree._insert(node.right, value)
        # update height of new tree
        node.height = 1 + max(BinaryTree._height(node.left), BinaryTree._height(node.right))
        return AVLTree._rebalance(node, value)

    @staticmethod
    def _rebalance(node, value):
        '''
        There are no test cases for the rebalance function,
        so you do not technically have to implement it.
        But both the insert function needs the rebalancing code,
        so I recommend including that code here.
        '''
        if AVLTree._balance_factor(node) > 1:
            if AVLTree._balance_factor(node.left) < 0:
                # if value >= node.left.value:
                node.left = AVLTree._left_rotate(node.left)
            node = AVLTree._right_rotate(node)
        if AVLTree._balance_factor(node) < -1:
            if AVLTree._balance_factor(node.right) > 0:
                # if value <= node.right.value:
                node.right = AVLTree._right_rotate(node.right)
            node = AVLTree._left_rotate(node)
        return node
