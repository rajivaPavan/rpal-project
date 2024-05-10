from interpreter.ast import ASTNode
from interpreter.cse_machine.st import STNode
from .ast.standardize import ASTStandardizer
from .cse_machine import CSEMachine
from .parser import RPALParser
from .lexer.tokens import *
from logger import logger 


class Interpreter:
    """
    Represents the Interpreter.
    
    Attributes: 
        __program: The source code.
        __switch: Switch specifying to print the ast or st.
        __ast: The abstract syntax tree.
        __st: The standardized tree.        
    """
    
    __AST_SWITCH = "-ast"
    __ST_SWITCH = "-st"
    
    def __init__(self, program, switch = None):
        self.__program = program
        self.__switch = switch
        self.__ast: ASTNode = None
        self.__st: STNode = None
    
    def interpret(self):
        """
        Interprets the given program.
        """
        res = ""
        try: 
            # Parse the program to get the ast
            self.__parse()
            if self.__switch == Interpreter.__AST_SWITCH:
                return
            # Get the st from the ast. 
            self.__standardize_ast()
            if self.__switch != Interpreter.__ST_SWITCH:
                self.__compute()            
        except Exception as e:
            logger.error(e)

    
    def __parse(self):
        """
        Parses the program given to the interpreter. Prints the AST if the switch is -ast.
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
        Standardizes the ast. Print the ST if the switch is -st.
        """
        standardizer = ASTStandardizer()
        self.__st = standardizer.standardize(self.__ast)
        
        if self.__switch == Interpreter.__ST_SWITCH:
            print(self.__st)

    def __compute(self):
        """
        Computes the result by inputting the standardized tree (ST) to the CSE machine.
        """
        st = self.__st
        cse = CSEMachine(st)
        try:
            cse.evaluate()
        except ZeroDivisionError as e:
            print("Zero Division Error: Division by zero")
        except RecursionError as e:
            print("Recursion Error: Maximum recursion depth exceeded")

