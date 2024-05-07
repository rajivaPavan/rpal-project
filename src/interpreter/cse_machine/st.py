from interpreter.ast.nodes import Nodes
from interpreter.lexer.tokens import Token
from structs.tree import BinaryTreeNode

    
class STNode(BinaryTreeNode):
    """A class representing a node in a Standardized Tree (ST).
    
    The STNode class uses the left child right sibling representation to store the tree structure.
    Each node contains a reference to its node value, left child, and right sibling.
    """

    @staticmethod
    def createFCRSNode(value, left:BinaryTreeNode= None, right:BinaryTreeNode = None):
        """
        Create node with left as first child and right as sibling of first child
        """
        left.setRight(right) 
        node = STNode(value, left, None)
        return node
    
    @staticmethod
    def gamma_node(left = None, right = None):
        """
        Creates a new gamma node in the form of a FCRS node.
        """
        return STNode.createFCRSNode(Nodes.GAMMA, left, right)
    
    @staticmethod
    def lambda_node(left = None, right = None):
        """
        Creates a new lambda node in the form of a FCRS node.
        """
        return STNode.createFCRSNode(Nodes.LAMBDA, left, right)
    
    def is_lambda(self):
        return self.isValue(Nodes.LAMBDA)
    
    def is_gamma(self):
        return self.isValue(Nodes.GAMMA)
    
    def is_conditional(self):
        return self.isValue(Nodes.COND)
    
    def is_tau(self):
        return self.isValue(Nodes.TAU)
    
    @staticmethod
    def assign_node(left = None, right = None):
        """
        Creates a new assign node in the form of a FCRS node.
        """
        return STNode.createFCRSNode(Nodes.ASSIGN, left, right)
        
    @staticmethod
    def ystar_node():
        """
        Creates a new ystar node in the form of a FCRS node.
        """
        return STNode(Nodes.YSTAR)
    
    def parseValueInToken(self):
        token = self.getValue()
        if not isinstance(token, Token):
            return token
        return token.getValue()
    
    def getSibilingCount(self):
        count = 0
        right = self.getRight()
        while right is not None:
            count += 1
            right = right.getRight()
        return count
    
    def getChildrenCount(self):
        count = 0
        left = self.getLeft()
        while left is not None:
            count += 1
            left = left.getRight()
        return count
    
    

            

    
    
        
    
 