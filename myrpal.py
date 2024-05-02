
import sys
from rpal_interpreter import Interpreter
from helpers import *

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