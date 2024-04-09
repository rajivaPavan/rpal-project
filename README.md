# rpal-project

The project is to implement a lexical analyzer and parser for an RPAL language using Python. The lexical analyzer will read the input file and generate a list of tokens. The parser will read the list of tokens and generate an abstract syntax tree (AST). The AST will be used to generate the output in the form of a tree.

# Usage 

To run the program, use the following command:

```bash
python myrpal.py simple
```

to print the ast, add the `-ast` flag at the end of the command
```bash
python myrpal.py simple -ast
```

In Linux, run the command by replacing `python` with `python3`

## Testing

To run the tests, navigate to the root directory of the project and use the following commands.



```bash
# lexer tests
python -m unittest tests/test_lexer.py

# parser tests
python -m unittest tests/test_parser.py
python -m unittest tests/test_rpal_parser.py

# all
python3 -m unittest discover -s tests -p 'test_*.py'

# error tests
python myrpal.py tests/errors/error_1 -ast
```