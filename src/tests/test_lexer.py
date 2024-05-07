# test/test_lexer.py
import unittest
from interpreter.lexer import Lexer
from __helpers import read_file
from interpreter.lexer.tokens import InvalidTokenException

class TestLexer(unittest.TestCase):

    def test_lex(self):
        src = read_file("tests/parser/test")
        lexer = Lexer(src)
        expected = "[(<KEYWORD>, 'let'), (<IDENTIFIER>, 'Sum'), ((, None), (<IDENTIFIER>, 'A'), (), None), (<OPERATOR>, '='), (<IDENTIFIER>, 'Psum'), ((, None), (<IDENTIFIER>, 'A'), (,, None), (<IDENTIFIER>, 'Order'), (<IDENTIFIER>, 'A'), (), None), (<KEYWORD>, 'where'), (<KEYWORD>, 'rec'), (<IDENTIFIER>, 'Psum'), ((, None), (<IDENTIFIER>, 'T'), (,, None), (<IDENTIFIER>, 'N'), (), None), (<OPERATOR>, '='), (<IDENTIFIER>, 'N'), (<KEYWORD>, 'eq'), (<INTEGER>, '0'), (<OPERATOR>, '->'), (<INTEGER>, '0'), (<OPERATOR>, '|'), (<IDENTIFIER>, 'Psum'), ((, None), (<IDENTIFIER>, 'T'), (,, None), (<IDENTIFIER>, 'N'), (<OPERATOR>, '-'), (<INTEGER>, '1'), (), None), (<OPERATOR>, '+'), (<IDENTIFIER>, 'T'), (<IDENTIFIER>, 'N'), (<KEYWORD>, 'in'), (<IDENTIFIER>, 'Print'), ((, None), (<IDENTIFIER>, 'Sum'), ((, None), (<INTEGER>, '1'), (,, None), (<INTEGER>, '2'), (,, None), (<INTEGER>, '3'), (,, None), (<INTEGER>, '4'), (,, None), (<INTEGER>, '5'), (), None), (), None)]"
        self.assertEqual(str(lexer.tokenize()), expected)
        
    def test_lex_one_token(self):
        src = read_file("tests/parser/test")
        lexer = Lexer(src)
        expected = "let"
        self.assertEqual(str(lexer.nextToken()), expected)
        
    def test_nextToken(self):
        src = read_file("tests/parser/test")
        lexer = Lexer(src)
        expected = "let"
        self.assertEqual(str(lexer.nextToken()), expected)
        expected = "<ID:Sum>"
        self.assertEqual(str(lexer.nextToken()), expected)
        
    def test_lex_two_tokens(self):
        src = read_file("tests/parser/test")
        lexer = Lexer(src)
        expected = "[(<KEYWORD>, 'let'), (<IDENTIFIER>, 'Sum')]"
        self.assertEqual(str(lexer.tokenize(count=2)), expected)

    def test_lex_empty(self):
        src = ""
        lexer = Lexer(src)
        self.assertEqual(lexer.tokenize(), [])
               
    def test_lex_comment(self):
        src = "// this is a comment\n3+5"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<INTEGER>, '3'), (<OPERATOR>, '+'), (<INTEGER>, '5')]")
    
    def test_lex_comment_2(self):
        src = "3+5\n// this is a comment\n"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<INTEGER>, '3'), (<OPERATOR>, '+'), (<INTEGER>, '5')]")
    
    def test_lex_simple(self):
        src = "3 + 5 * (10 - 4)"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<INTEGER>, '3'), (<OPERATOR>, '+'), (<INTEGER>, '5'), (<OPERATOR>, '*'), ((, None), (<INTEGER>, '10'), (<OPERATOR>, '-'), (<INTEGER>, '4'), (), None)]")

            
    def test_lex_invalid_token(self):
        src = read_file("tests/lexer/invalid_token")
        lexer = Lexer(src)
        
        # check if exception is raised
        with self.assertRaises(InvalidTokenException):
            lexer.tokenize()
            
        # check if exception message is correct
        lexer.reset()
        try:
            lexer.tokenize()
        except Exception as e:
            self.assertEqual(str(e), "Invalid token at line 1, char 2")
        
    def test_integer_token(self):
        src = "123"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<INTEGER>, '123')]")
        
    def test_operator_token(self):
        src = "+"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<OPERATOR>, '+')]")
        
    def test_string_token(self):
        src = "'hello ++ @ 123'"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<STRING>, \"'hello ++ @ 123'\")]")        
    
    def test_strings(self):
        src = read_file("tests/lexer/strings")
        lexer = Lexer(src)
        expected = "[(<STRING>, \"'Positive'\"), (<OPERATOR>, '|'), (<IDENTIFIER>, 'x'), (<STRING>, \"'ab'\"), (<KEYWORD>, 'in')]"
        self.assertEqual(str(lexer.tokenize()),expected)
                         
    def test_lex_paren(self):
        src = "( )"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[((, None), (), None)]")
        
    def test_lex_semicolon(self):
        src = "a;"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<IDENTIFIER>, 'a'), (;, None)]")
        
    def test_lex_comma(self):
        src = "a, b"
        lexer = Lexer(src)
        self.assertEqual(str(lexer.tokenize()), "[(<IDENTIFIER>, 'a'), (,, None), (<IDENTIFIER>, 'b')]")
        
    def test_lex_spaces(self):
        src = "  \t \n\n\n  \t  "
        lexer = Lexer(src)
        self.assertEqual(lexer.tokenize(), [])

    def test_lookAhead_default(self):
        src = read_file("tests/parser/test")
        lexer = Lexer(src)
        expected = "let"
        self.assertEqual(str(lexer.lookAhead()), expected)

    def test_lookAhead_multiple_calls(self):
        src = read_file("tests/parser/test")
        lexer = Lexer(src)
        expected = "let"
        self.assertEqual(str(lexer.lookAhead()), expected)
        expected = "let"
        self.assertEqual(str(lexer.lookAhead()), expected)

    def test_lookAhead_empty(self):
        src = ""
        lexer = Lexer(src)
        self.assertEqual(lexer.lookAhead(), None)

    def test_lookAhead_comment(self):
        src = "// this is a comment\n3+5"
        lexer = Lexer(src)
        expected = "<INT:3>"
        self.assertEqual(str(lexer.lookAhead()), expected)

    def test_lookAhead_comment_2(self):
        src = "3+5\n// this is a comment\n"
        lexer = Lexer(src)
        expected = "<INT:3>"
        self.assertEqual(str(lexer.lookAhead()), expected)

    def test_lookAhead_simple(self):
        src = "3 + 5 * (10 - 4)"
        lexer = Lexer(src)
        expected = "<INT:3>"
        self.assertEqual(str(lexer.lookAhead()), expected)
        
    def test_lookAhead_after_nextToken(self):
        src = read_file("tests/parser/test")
        lexer = Lexer(src)
        self.assertEqual(str(lexer.nextToken()), "let")
        self.assertEqual(str(lexer.lookAhead()), "<ID:Sum>")


if __name__ == '__main__':
    unittest.main()