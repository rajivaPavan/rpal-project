from interpreter.ast import ASTNode
from interpreter.cse_machine.st import STNode
from .nodes import Nodes
from structs.tree import BinaryTreeNode


class ASTStandardizer:
    """
    A class that standardizes an Abstract Syntax Tree (AST).
    """

    def __init__(self):
        self.st:STNode = None  # Standardized Tree

    def standardize(self, ast:ASTNode)->STNode:
        """
        Standardizes the given AST.

        Args:
            ast: The input Abstract Syntax Tree (AST) to be standardized.

        Returns:
            Root of the standardized tree.
        """
        self.st = self.__standardize(ast)
        return self.st
        
    # list of values of nodes that do not need to be standardized
    NON_STANDARDIZE = Nodes.UOP + Nodes.BOP + [
        Nodes.GAMMA, Nodes.TAU, Nodes.COND, Nodes.COMMA,
        Nodes.TRUE,Nodes.FALSE, Nodes.DUMMY, Nodes.NIL,
        Nodes.ASSIGN
    ]

    @staticmethod
    def check_to_standardize(node:BinaryTreeNode):
        
        node_value = node.getValue()

        # false if the node_value is a name <ID:...> or an integer <INT:...>
        if node.is_name():
            return False
        
        if node_value in ASTStandardizer.NON_STANDARDIZE:
            return False
        
        return True

    def __standardize(self, node:BinaryTreeNode):
        """"
        standardize the AST using post order traversal.
        
        AST given by the parser is in the form of a first child right sibling tree.
        Standardized tree is in the form of a binary tree.
        """
        
        if node is None:
            return None
        
        left = self.__standardize(node.getLeft())
        right = self.__standardize(node.getRight())
        node.setLeft(left)
        
        transformed_node = None
        # if the node is a non standardize node, return a copy of it
        if not ASTStandardizer.check_to_standardize(node):
            transformed_node = STNode.copy(node)
        else:
            # apply the relevent subtree transformation based on the node
            transformed_node = self.__apply_transformation(node)
        
        transformed_node.setRight(right)
        
        return transformed_node
        
    def __apply_transformation(self, node:BinaryTreeNode) -> STNode:
        """Calls the relevant transformation function based on the node value."""
        node_value = node.getValue()
        res = None
        
        if node_value == Nodes.LET:
            res = self.__transform_let(node)
        elif node_value == Nodes.WITHIN:
            res = self.__transform_within(node)
        elif node_value == Nodes.FCN_FORM:
            res = self.__transform_fcn_form(node)
        elif node_value == Nodes.LAMBDA:
            res = self.__transform_lambda(node)
        elif node_value == Nodes.AND:
            res = self.__transform_and(node)
        elif node_value == Nodes.WHERE:
            res = self.__transform_where(node)
        elif node_value == Nodes.REC:
            res = self.__transform_rec(node)
        elif node_value == Nodes.AT:
            res = self.__transform_at(node)
        else:
            raise Exception(f"Node value {node_value} not handled")

        return res
    
    def __transform_let(self, node:BinaryTreeNode):
        left:STNode = node.getLeft()
        p = left.getRight()

        x:STNode = left.getLeft()
        e = x.getRight()

        lambda_ = STNode.lambda_node(x, p)
        gamma = STNode.gamma_node(lambda_, e)

        return gamma

    def __transform_within(self, node:BinaryTreeNode):
        left_assign:STNode = node.getLeft()
        right_assign:STNode = left_assign.getRight()
        
        x1:STNode = left_assign.getLeft()
        e1:STNode = x1.getRight()
        x2:STNode = right_assign.getLeft()
        e2:STNode = x2.getRight()

        lambda_ = STNode.lambda_node(x1, e2)
        gamma = STNode.gamma_node(lambda_, e1)
        assign_node = STNode.assign_node(x2, gamma)
        return assign_node

    def __transform_fcn_form(self, node:BinaryTreeNode):
        p:STNode = node.getLeft()
        v_node = p.getRight()
        lambda_ = ASTStandardizer.__transform_lambda_helper(v_node)
        transformed_node = STNode.assign_node(p, lambda_)
        return transformed_node

    @staticmethod
    def __transform_lambda_helper(v_node:BinaryTreeNode)->STNode:
        if v_node.getRight() is None:
            return v_node
        
        subtree = ASTStandardizer.__transform_lambda_helper(v_node.getRight())
        lambda_node = STNode.lambda_node(v_node, subtree)
        return lambda_node

    def __transform_lambda(self, node:BinaryTreeNode):
        lambda_left:STNode = node.getLeft()

        # handle the second lambda transform that has ,
        if lambda_left.isValue(Nodes.COMMA):
            return STNode.copy(node)
        
        lambda_ = ASTStandardizer.__transform_lambda_helper(lambda_left)
        return lambda_

    def __transform_and(self, node:BinaryTreeNode):
        x_nodes = []
        e_nodes = []
        child_assign_node = node.getLeft()
        while child_assign_node is not None:
            x = child_assign_node.getLeft()
            e = x.getRight()
            x_nodes.append(x)
            e_nodes.append(e)
            child_assign_node = child_assign_node.getRight()
        
        x_siblings = STNode.siblings(x_nodes)
        e_siblings = STNode.siblings(e_nodes)
        comma_node = STNode.comma_node(x_siblings)
        tau_node = STNode.tau_node(e_siblings)
        assign_node = STNode.assign_node(comma_node, tau_node)
        return assign_node

    def __transform_where(self, node:BinaryTreeNode):
        p:STNode = node.getLeft()
        assign_node: STNode = p.getRight()
        x:STNode = assign_node.getLeft()
        e:STNode = x.getRight()
        p.setRight(None) # remove the assign node from p
        lambda_ = STNode.lambda_node(x, p)
        gamma = STNode.gamma_node(lambda_, e)
        return gamma

    def __transform_rec(self, node:BinaryTreeNode):
        assign_node:STNode = node.getLeft() # only child
        original_x:STNode = assign_node.getLeft()
        x1 = STNode.deep_copy(original_x)
        x2 = STNode.deep_copy(original_x)
        e:STNode = original_x.getRight()

        y_star = STNode.ystar_node()
        lambda_ = STNode.lambda_node(x1, e)
        gamma = STNode.gamma_node(y_star, lambda_)
        assign_node = STNode.assign_node(x2, gamma)
        return assign_node

    def __transform_at(self, node:BinaryTreeNode):
        e1:STNode = node.getLeft()
        n:STNode = e1.getRight()
        e2:STNode = n.getRight()
        e1.setRight(None) # remove n from e1
        gamma = STNode.gamma_node(n, e1)
        gamma = STNode.gamma_node(gamma, e2)
        return gamma 



