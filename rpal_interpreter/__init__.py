from rpal_interpreter.ast_standardizer import ASTStandardizer
from rpal_interpreter.trees import ASTNode, STNode
from .lexer import *
from .rpal_parser import RPALParser
from .tokens import *

class Interpreter:
    
    __AST_SWITCH = "-ast"
    __ST_SWITCH = "-st"
    
    def __init__(self, program, switch = None):
        self.__program = program
        self.__switch = switch
        self.__ast: ASTNode = None
        self.__st: STNode = None
        self.__result = ""
    
    def interpret(self):
        """
        Interpret the given program
        
        args: 
            program - the source code
            switch - switch specifying to print the ast or st
        """
        res = ""
        try: 
            # Parse the program to get the ast
            self.__parse()
            # Get the st from the ast
            self.__standardize_ast()
        
            # Print the ast or st
            if self.__switch is None:
                self.__compute()
            
        except Exception as e:
            print(e)

        return
    
    def __parse(self):
        """
        Parse the program given to the interpreter. Also print the AST if the switch is -ast
        """
        
        parser = RPALParser(self.__program)

        self.__ast = parser.parse()
        
        # Check if the program was fully parsed
        if parser.nextToken() != None:
            if self.__switch is Interpreter.__AST_SWITCH:
                print(self.__ast)
            raise BuiltTreeException("Program was not fully parsed.")
        
        if self.__switch == Interpreter.__AST_SWITCH:
            print(self.__ast)
             
    def __standardize_ast(self):
        """
        Standardize the ast. Also print the ST if the switch is -st
        """
        standardizer = ASTStandardizer()
        self._st = standardizer.standardize(self.__ast)
        
        if self.__switch == Interpreter.__ST_SWITCH:
            print(self.__st)

    def __compute(self):
            """
            Computes the result by inputting the standardized tree (ST) to the CSE machine.
            """
            st = self.__st
            
            # input the ST to a CSE machine and get the result

            print("computed result")

