import unittest
from rpal_interpreter.rpal_parser import RPALParser

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
    
if __name__ == '__main__':
    unittest.main()