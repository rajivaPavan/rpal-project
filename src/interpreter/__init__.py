from interpreter.ast import ASTNode
from interpreter.cse_machine.st import STNode
from .ast.standardize import ASTStandardizer
from .cse_machine import CSEMachine
from .parser import RPALParser
from .lexer.tokens import *
from logger import logger 


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

        try: 
            # Parse the program to get the ast
            self.__parse()
            if self.__switch == Interpreter.__AST_SWITCH:
                # exit if the switch is -ast
                return

            # Get the st from the ast
            self.__standardize_ast()

            if self.__switch != Interpreter.__ST_SWITCH:
                # Compute the result if no switch is given
                self.__compute()            

        except Exception as e:
            logger.error(e)

    
    def __parse(self):
        """
        Parse the program given to the interpreter. Also print the AST if the switch is -ast
        """
        
        parser = RPALParser(self.__program)
        try:
            self.__ast = parser.parse()

            # Check if the program was fully parsed
            if parser.nextToken() != None:
                if self.__switch is Interpreter.__AST_SWITCH:
                    print(self.__ast)
                raise BuiltTreeException("Program was not fully parsed.")
        
        except (InvalidTokenException, 
                BuildTreeException, BuiltTreeException) as e:
            print(e)
            raise e
        
        except Exception as e:
            print("An error occured while parsing the program.")
            raise e
        
        if self.__switch == Interpreter.__AST_SWITCH:
            print(self.__ast)
             
    def __standardize_ast(self):
        """
        Standardize the ast. Also print the ST if the switch is -st
        """
        standardizer = ASTStandardizer()

        try:
            self.__st = standardizer.standardize(self.__ast)

        except Exception as e:
            print("An error occured while standardizing the AST.")
            raise e
        
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
            except RecursionError as e:
                print("Recursion Error: Maximum recursion depth exceeded")
                raise e
            except (ZeroDivisionError, ArithmeticError) as e:
                print(e)
                raise e
            except Exception as e:
                print("An error occured while computing the result.")
                raise e
