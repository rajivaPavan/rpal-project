
import sys
from rpal_interpreter import Interpreter
from helpers import *


def init_args(args):
    if len(args) < 2:
        print("Usage: python3 myrpal.py <file_name> [-ast]")
        return
    
    file_name = args[1]
    has_ast_switch = args[-1] == "-ast"
    return file_name, has_ast_switch

def main():
    """Entry point for the RPAL lexical analyzer and parser."""

    # initialize args
    args = sys.argv
    file_name, ast_switch = init_args(args)

    # Read the file "file_name"
    program = read_file(file_name)

    interpreter = Interpreter()
    interpreter.interpret(program, ast_switch)

    return

if __name__ == "__main__":
    main()