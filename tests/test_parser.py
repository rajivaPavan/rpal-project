import unittest
from rpal_interpreter.parser import Parser
from helpers import *

class TestParser(unittest.TestCase):
    
    def test_ast_str(self):
        src = read_file("file_name")
        parser = Parser(src)
        parser.read(parser.nextToken())
        parser.buildTree("gamma", 1)
        parser.read(parser.nextToken())
        parser.read(parser.nextToken())
        parser.buildTree("gamma", 2)
        parser.buildTree("program", 2)
        ast = parser.getAST()
        self.assertEqual(str(ast),
"""program
.gamma
..<ID:let>
.gamma
..<ID:Sum>
..((, None)""")