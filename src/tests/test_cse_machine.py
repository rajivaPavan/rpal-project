import os
import subprocess
import unittest

class TestRPALSTGeneration(unittest.TestCase):
    def run_rpal(self, filename):
        """ Helper function to run the RPAL parser with the -st flag """
        result = subprocess.run(['python', './myrpal.py', filename], capture_output=True, text=True)
        return result.stdout.strip()

    def test_cse_machine(self):
        """ Test the AST generation against expected output files """
        
        test_files = [
            ("tests/machine/ex1", "tests/machine/ex1.out"),
            ("tests/machine/ex2", "tests/machine/ex2.out"),
            ("tests/machine/ex3", "tests/machine/ex3.out"),
            ("tests/machine/ex4", "tests/machine/ex4.out"),
            ("tests/machine/ex5", "tests/machine/ex5.out"),
            ("tests/rpal/rpal_01", "tests/rpal/output01.test"),
            ("tests/rpal/rpal_02", "tests/rpal/output02.test"),
            ("tests/rpal/rpal_04", "tests/rpal/output04.test"),
            ("tests/rpal/rpal_05", "tests/rpal/output05.test"),
            ("tests/rpal/rpal_07", "tests/rpal/output07.test"),
            ("tests/rpal/rpal_08", "tests/rpal/output08.test"),
            ("tests/machine/aug", "tests/machine/aug.out"),
            ("tests/machine/infix", "tests/machine/infix.out"),
            ("tests/machine/infix2", "tests/machine/infix2.out"),
            ("tests/st/add", "tests/st/add.out"),
            ("tests/st/fact3", "tests/st/fact3.out"),
            ("tests/machine/towers", "tests/machine/towers.out")
        ]

        for input_file, expected_file in test_files:
            # check if input file exists
            with self.subTest(input_file=input_file):
                with open(expected_file) as file:
                    expected_output = file.read().strip()
                    ast_output = self.run_rpal(input_file)
                    self.assertEqual(ast_output, expected_output)
