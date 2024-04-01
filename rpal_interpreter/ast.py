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
        
    def __str__(self):
        s = str(self.node) 
        if self.left_child != None:
            s += "\n.." + str(self.left_child)
        if self.right_sibling != None:
            s += "\n.." + str(self.right_sibling)
        return s
 