import unittest
from rpal_interpreter.rpal_parser import RPALParser
from helpers import *
class TestRPALParser(unittest.TestCase):
    
    def test_Rn(self):
        
        test_cases = [
            ("x", "<ID:x>"),
            ("1", "<INT:1>"),
            ("\"hello\"", "<STR:\"hello\">"),
            ("true", "true"),
            ("false", "false"),
            ("nil", "nil"),
            ("dummy", "dummy"),
        ]
        
        for src, expected_ast in test_cases:
            parser = RPALParser(src)
            parser.proc_Rn()
            ast = parser.getAST()
            self.assertEqual(str(ast), expected_ast)

    def test_Rn_empty(self):
        src = " \n"
        self.assertRaises(Exception, RPALParser(src))
            
    def test_R(self):
        
        test_cases = [
            (" x y", "gamma\n.<ID:x>\n.<ID:y>"),
            (" x y z", "gamma\n.<ID:x>\n.<ID:y>\n.<ID:z>"),
        ] 

        for src, expected_ast in test_cases:
            parser = RPALParser(src)
            parser.proc_R()
            ast = parser.getAST()
            self.assertEqual(str(ast), expected_ast)
    
    def test_Vl(self):
        src = "x , y, z"
        parser = RPALParser(src)
        parser.proc_Vl()
        ast = parser.getAST()
        self.assertEqual(str(ast), ",\n.<ID:x>\n.<ID:y>\n.<ID:z>")
        
    def test_Vb(self):
        tests = [("x", "<ID:x>"), 
                 ("(x, y)", ",\n.<ID:x>\n.<ID:y>"),
                 ("()", "()")]
        
        for src, expected_ast in tests:
            parser = RPALParser(src)
            parser.proc_Vb()
            ast = parser.getAST()
            self.assertEqual(str(ast), expected_ast)
            
    def test_E_1(self):
        src= """Psum (A,Order A )"""
        parser = RPALParser(src)
        ast = parser.parse()
        self.assertEqual(str(ast), """gamma
.<ID:Psum>
.tau
..<ID:A>
..gamma
...<ID:Order>
...<ID:A>""")
        
    def test_D(self):
        src = read_file("tests/parser/test_D")
        parser = RPALParser(src)
        ast = parser.parse()
        out = read_file("tests/parser/test_D_out").rstrip('\n')
        self.assertEqual(str(ast), out)
                
        
if __name__ == '__main__':
    unittest.main()