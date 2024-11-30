from interpreter.ast import ASTNode
from interpreter.cse_machine.st import STNode
from .ast.standardize import ASTStandardizer
from .cse_machine import CSEMachine, MachineException
from .parser import RPALParser
from .lexer.tokens import *
from logger import logger
import io
import sys

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

    def get_ast(self):
        return self.__ast

    def get_tree(self, tree):
        if(tree == Interpreter.__AST_SWITCH):
            return self.__ast
        else:
            return self.__st

    def get_result(self, format):
        if(format == Interpreter.__AST_SWITCH):
            return self.__ast
        elif(format == Interpreter.__ST_SWITCH):
            return self.__st
        else:
            return self.__output

    def interpret(self):
        """
        Interprets the given program.
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
                # Compute the result if no switch is given, capture the output from stdout
                original_stdout = sys.stdout
                stdout_capture = io.StringIO()
                sys.stdout = stdout_capture
                self.__compute()
                sys.stdout = original_stdout
                captured_output = stdout_capture.getvalue()
                stdout_capture.close()
                self.__output = captured_output

        except Exception as e:
            logger.error(e)


    def __parse(self):
        """
        Parses the program given to the interpreter. Prints the AST if the switch is -ast.
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
        Standardizes the ast. Print the ST if the switch is -st.
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
            except (MachineException) as e:
                print(e)
                raise e
            except Exception as e:
                print("An error occured while computing the result.")
                raise e
