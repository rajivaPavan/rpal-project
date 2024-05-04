from rpal_interpreter.nodes import Nodes
from rpal_interpreter.trees import BinaryTreeNode, STNode, ASTNode


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
        Nodes.TAU, Nodes.ARROW, Nodes.COMMA,
        Nodes.TRUE,Nodes.FALSE, Nodes.DUMMY, Nodes.NIL
    ]

    @staticmethod
    def check_to_standardize(node:BinaryTreeNode):
        
        node_value = str(node.getValue())

        # false if the node_value is a name <ID:...> or an integer <INT:...>
        if str.startswith(node_value, "<ID:") or str.startswith(node_value, "<INT:") or str.startswith(node_value, "<STR:"):
            return False
        
        if node_value in ASTStandardizer.NON_STANDARDIZE:
            return False
        
        return True

    def __standardize(self, node:BinaryTreeNode):
        # standardize the AST using post order traversal
        # AST given by the parser is in the form of a first child right sibling tree
        # Standardized tree is in the form of a binary tree
        if node is None:
            return None
        
        # standardize the left subtree
        left = self.__standardize(node.getLeft())
        node.setLeft(left)

        # standardize the right subtree
        right = self.__standardize(node.getRight())
        node.setRight(right)

        # if the node is a non standardize node, return a copy of it
        if not ASTStandardizer.check_to_standardize(node):
            return STNode.copy(node)
        
        # apply the relevent subtree transformation based on the node
        return self.__apply_transformation(node)
        
    def __apply_transformation(self, node:BinaryTreeNode) -> STNode:
        node_value = node.getValue()
        res = None
        
        if node_value == Nodes.GAMMA:
            res = STNode.copy(node)
        elif node_value == Nodes.LET:
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
        lamda_like = STNode.lambda_node(p.getRight(), None)
        lambda_ = self.__transform_lambda(lamda_like)
        return STNode.assign_node(p, lambda_)
        

    def __transform_lambda(self, node:BinaryTreeNode):
        lambda_left:STNode = node.getLeft()

        # handle the second lambtra transform that has ,
        if lambda_left.valueIs(Nodes.COMMA):
            return STNode.copy(node)
        
        def __transform_lambda_helper(node:BinaryTreeNode):
            if node.getRight() is None:
                return node
            
            v = node
            subtree = __transform_lambda_helper(node.getRight())
            lambda_node = STNode.lambda_node(v, subtree)
            return lambda_node
        
        lambda_left = __transform_lambda_helper(lambda_left)
        lambda_left.setRight(node.getRight())
        return lambda_left

    def __transform_and(self, node:BinaryTreeNode):
        raise Exception("transform_and() Not implemented")

    def __transform_where(self, node:BinaryTreeNode):
        p:STNode = node.getLeft()
        assign_node: STNode = p.getRight()
        x:STNode = assign_node.getLeft()
        e:STNode = x.getRight()

        lambda_ = STNode.lambda_node(x, p)
        gamma = STNode.gamma_node(lambda_, e)
        return gamma

    def __transform_rec(self, node:BinaryTreeNode):
        raise Exception("transform_rec() Not implemented")

    def __transform_at(self, node:BinaryTreeNode):
        e1:STNode = node.getLeft()
        n:STNode = e1.getRight()
        e2:STNode = n.getRight()

        gamma = STNode.gamma_node(n, e1)
        gamma = STNode.gamma_node(gamma, e2)
        return gamma 



