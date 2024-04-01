class ASTNode:
    """left child right sibling representation"""
       
    def __init__(self, node, left_child=None, right_sibling=None):
        self.node = node
        self.left_child = left_child
        self.right_sibling = right_sibling
        
    def setLeftChild(self, node):
        self.left_child = node
        
    def setRightSibling(self, node):
        self.right_sibling = node
        
    def __str__(self, level=0):
        s = str(self.node)
        if self.left_child != None:
            child_level = level + 1
            s += "\n" + "."*child_level + self.left_child.__str__(child_level)
        if self.right_sibling != None:
            s += "\n" + "."*level + self.right_sibling.__str__(level)
        return s
 