from .lexer import Lexer
from .parser import Parser

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

        self.program = program
        self.ast_switch = ast_switch
        # Get the tokens from the lexer
        lexer = Lexer()
        tokens = lexer.lex(self.program)
        print("Tokens: ", tokens)

        # # Get the ast from the parser
        # parser = Parser(tokens)
        # ast = parser.parse()

        # self.result(ast, ast_switch)

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

