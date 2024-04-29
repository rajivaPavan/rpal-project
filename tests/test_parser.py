import unittest
from rpal_interpreter.parser import Parser
from rpal_interpreter.rpal_parser import RPALParser
from helpers import *

class TestParser(unittest.TestCase):
    
    def test_ast_str(self):
        src = "let Sum("
        parser = Parser(src)
        parser.read(parser.nextToken(), ignore=False)
        parser.buildTree("gamma", 1)
        parser.read(parser.nextToken(), ignore=False)
        parser.read(parser.nextToken(), ignore=False)
        parser.buildTree("gamma", 2)
        parser.buildTree("program", 2)
        ast = parser.getAST()
        self.assertEqual(str(ast),
"""program
.gamma
..let
.gamma
..<ID:Sum>
..\"(\"""")