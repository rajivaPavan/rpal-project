from .parser import Parser

class RPALParser(Parser):
    def __init__(self,src):
        super().__init__(src)
        
    def parse(self):
        """returns the AST of the src program"""
        return self.getAST()
    
