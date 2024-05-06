import os
import subprocess
import unittest

class TestRPALSTGeneration(unittest.TestCase):
    def run_rpal(self, filename):
        """ Helper function to run the RPAL parser with the -st flag """
        result = subprocess.run(['python3', './myrpal.py', filename], capture_output=True, text=True)
        return result.stdout.strip()

    def test_cse_machine(self):
        """ Test the AST generation against expected output files """
        
        test_files = [
            ("tests/machine/ex1", "tests/machine/ex1.out"),
            ("tests/machine/ex2", "tests/machine/ex2.out"),
            ("tests/machine/ex3", "tests/machine/ex3.out"),
        ]

        for input_file, expected_file in test_files:
            # check if input file exists
            with self.subTest(input_file=input_file):
                with open(expected_file) as file:
                    expected_output = file.read().strip()
                    ast_output = self.run_rpal(input_file)
                    self.assertEqual(ast_output, expected_output)
