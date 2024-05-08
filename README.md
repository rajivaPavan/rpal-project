# rpal-project

The project is to implement a lexical analyzer and parser for an RPAL language using Python. The lexical analyzer will read the input file and generate a list of tokens. The parser will read the list of tokens and generate an abstract syntax tree (AST). The AST will be used to generate the output in the form of a tree.

# Usage 
Navigate to the `/src` directory of the project.
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

To run the tests, navigate to the `/src` of the project and use the following commands.



```bash
# lexer tests
python -m unittest tests/test_lexer.py

# parser tests
python -m unittest tests/test_parser.py
python -m unittest tests/test_rpal_parser.py

# all
python -m unittest discover -s tests -p 'test_*.py'

```

# Documentation

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