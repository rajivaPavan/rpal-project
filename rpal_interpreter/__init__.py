from .lexer import Lexer
from .rpal_parser import RPALParser

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, program, ast_switch = False):
        """
        Interpret the given program
        
        args: 
            program - the source code
            ast_switch - whether to print the ast or the result
        """
        
        # Get the ast from the parser
        parser = RPALParser(program)
        ast = parser.parse()

        self.result(ast, ast_switch)

        return
        
    def result(self, ast, has_ast_switch):
        """Print the ast or the result"""
        if has_ast_switch:
            print(ast)
        else:
            output = Interpreter.__compute(ast)
            print(output)

    def __compute(ast):
        return "computed result"

