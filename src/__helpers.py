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

__RUN_COMMAND_USAGE = "Usage: python3 myrpal.py [-ast, -st] <file_name>\nRequired: <file_name>\nOptional: -as"

def init_args(args)->Tuple[str, str]:
    
    """Takes command line arguments as input and returns the file name and switch"""
    
    switch:str = None
    file_name = ""
    
    if len(args) < 2:
        print(__RUN_COMMAND_USAGE)
        exit(1)
    
    if len(args) > 2:
        file_name = args[2]
        if str.startswith(args[1], "-"):
            switch = args[1]
    else:
        file_name = args[1]
        
    return file_name, switch