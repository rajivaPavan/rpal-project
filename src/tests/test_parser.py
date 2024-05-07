import unittest
from interpreter.parser import Parser
from __helpers import read_file

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