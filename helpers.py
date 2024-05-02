from typing import Tuple


def read_file(file):
    """Reads a file and returns its contents."""
    try:
        with open(file, "r") as f:
            content = f.read()
            return content
    except FileNotFoundError:
        print(f"File {file} not found.")
        exit(1)

__RUN_COMMAND_USAGE = "Usage: python3 myrpal.py <file_name> [-ast]\nRequired: <file_name>\nOptional: -as"

def init_args(args):
    """
    Initializes the arguments for the program.

    Args:
        args (list): The command-line arguments.

    Returns:
        tuple: A tuple containing the file name and a boolean indicating whether the "-ast" switch is present.

    Raises:
        SystemExit: If the number of arguments is less than 1 or if the file name is "-ast".

    """

    has_ast_switch = False
    
    if len(args) < 2:
        print(__RUN_COMMAND_USAGE)
        exit(1)
    
    file_name = args[1]
    
    if len(args) > 2:
        has_ast_switch = args[2] == "-ast"
    
    return file_name, has_ast_switch