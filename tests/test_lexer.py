# test/test_lexer.py
import unittest
from rpal_interpreter.lexer import Lexer
from helpers import *
from rpal_interpreter.tokens import InvalidTokenException

class TestLexer(unittest.TestCase):

    def test_lex(self):
        lexer = Lexer()
        src = read_file("file_name")
        expected = "[(<IDENTIFIER>, 'let'), (<IDENTIFIER>, 'Sum'), ((, None), (<IDENTIFIER>, 'A'), (), None), (<OPERATOR>, '='), (<IDENTIFIER>, 'Psum'), ((, None), (<IDENTIFIER>, 'A'), (,, None), (<IDENTIFIER>, 'Order'), (<IDENTIFIER>, 'A'), (), None), (<IDENTIFIER>, 'where'), (<IDENTIFIER>, 'rec'), (<IDENTIFIER>, 'Psum'), ((, None), (<IDENTIFIER>, 'T'), (,, None), (<IDENTIFIER>, 'N'), (), None), (<OPERATOR>, '='), (<IDENTIFIER>, 'N'), (<IDENTIFIER>, 'eq'), (<INTEGER>, '0'), (<OPERATOR>, '->'), (<INTEGER>, '0'), (<OPERATOR>, '|'), (<IDENTIFIER>, 'Psum'), ((, None), (<IDENTIFIER>, 'T'), (,, None), (<IDENTIFIER>, 'N'), (<OPERATOR>, '-'), (<INTEGER>, '1'), (), None), (<OPERATOR>, '+'), (<IDENTIFIER>, 'T'), (<IDENTIFIER>, 'N'), (<IDENTIFIER>, 'in'), (<IDENTIFIER>, 'Print'), ((, None), (<IDENTIFIER>, 'Sum'), ((, None), (<INTEGER>, '1'), (,, None), (<INTEGER>, '2'), (,, None), (<INTEGER>, '3'), (,, None), (<INTEGER>, '4'), (,, None), (<INTEGER>, '5'), (), None), (), None)]"
        self.assertEqual(str(lexer.lex(src)), expected)

    def test_lex_empty(self):
        lexer = Lexer()
        src = ""
        self.assertEqual(lexer.lex(src), [])
               
    def test_lex_comment(self):
        lexer = Lexer()
        src = "// this is a comment\n3+5"
        self.assertEqual(str(lexer.lex(src)), "[(<INTEGER>, '3'), (<OPERATOR>, '+'), (<INTEGER>, '5')]")
    
    def test_lex_comment_2(self):
        lexer = Lexer()
        src = "3+5\n// this is a comment\n"
        self.assertEqual(str(lexer.lex(src)), "[(<INTEGER>, '3'), (<OPERATOR>, '+'), (<INTEGER>, '5')]")
    
    def test_lex_simple(self):
        lexer = Lexer()
        src = "3 + 5 * (10 - 4)"
        self.assertEqual(str(lexer.lex(src)), "[(<INTEGER>, '3'), (<OPERATOR>, '+'), (<INTEGER>, '5'), (<OPERATOR>, '*'), ((, None), (<INTEGER>, '10'), (<OPERATOR>, '-'), (<INTEGER>, '4'), (), None)]")

            
    def test_lex_invalid_token(self):
        lexer = Lexer()
        src = read_file("tests/lexer/invalid_token")
        
        # check if exception is raised
        with self.assertRaises(InvalidTokenException):
            lexer.lex(src)
            
        # check if exception message is correct
        try:
            lexer.lex(src)
        except Exception as e:
            self.assertEqual(str(e), "Invalid token at line 1, char 2")
        
    def test_integer_token(self):
        lexer = Lexer()
        src = "123"
        self.assertEqual(str(lexer.lex(src)), "[(<INTEGER>, '123')]")
        
    def test_operator_token(self):
        lexer = Lexer()
        src = "+"
        self.assertEqual(str(lexer.lex(src)), "[(<OPERATOR>, '+')]")
        
    def test_string_token(self):
        lexer = Lexer()
        src = "\"hello ++ @ 123\""
        self.assertEqual(str(lexer.lex(src)), "[(<STRING>, '\"hello ++ @ 123\"')]")        
    
    def test_lex_paren(self):
        lexer = Lexer()
        src = "( )"
        self.assertEqual(str(lexer.lex(src)), "[((, None), (), None)]")
        
    def test_lex_semicolon(self):
        lexer = Lexer()
        src = "a;"
        self.assertEqual(str(lexer.lex(src)), "[(<IDENTIFIER>, 'a'), (;, None)]")
        
    def test_lex_comma(self):
        lexer = Lexer()
        src = "a, b"
        self.assertEqual(str(lexer.lex(src)), "[(<IDENTIFIER>, 'a'), (,, None), (<IDENTIFIER>, 'b')]")
        
    def test_lex_spaces(self):
        lexer = Lexer()
        src = "  \t \n\n\n  \t  "
        self.assertEqual(lexer.lex(src), [])
    

if __name__ == '__main__':
    unittest.main()