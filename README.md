# RPAL Interpreter

This project aims to implement an RPAL interpreter in Python. The interpreter will be able to parse RPAL code, build an abstract syntax tree (AST), and execute the RPAL program.

## Features
- Lexical analysis of RPAL code
- Parsing RPAL code to build an abstract syntax tree (AST)
- Interpreting and executing RPAL programs
- Support for variable bindings, function definitions, conditionals, and recursion


## Usage 
Navigate to the `/src` directory of the project.
To run the program, use the following command:

```bash
python myrpal.py filename
```
where `filename` is the name of the file containing the RPAL code.

to print the abstract syntax tree, add the `-ast` flag at the end of the command

```bash
python myrpal.py filename -ast
```

to print the standardized tree, add the `-st` flag at the end of the command

```bash
python myrpal.py filename -st
```

In Linux, run the command by replacing `python` with `python3`

## Testing

To run the tests, navigate to the `/src` of the project and use the following commands.

```powershell
# lexer tests
python -m unittest tests/test_lexer.py

# parser tests
python -m unittest tests/test_parser.py
python -m unittest tests/test_rpal_parser.py

# ...

# all
python -m unittest discover -s tests -p 'test_*.py'
```

# Documentation

Documentation can be found at [https://rajivapavan.github.io/rpal-project/](https://rajivapavan.github.io/rpal-project/)

Documentation is built using Sphinx.

To build the documentation,
enable the virtual environment

```powershell
python -m venv venv ; .\venv\Scripts\Activate
```

install the required packages
```powershell
pip install -r requirements.txt
```

From the root directory of the project, run the following commands:
```bash
cd docs
sphinx-apidoc -o . ../src
./make html # or whatever format you want
```
to find list of available formats, run
```bash
./make
```