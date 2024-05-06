import os
import subprocess
import unittest

class TestRPALSTGeneration(unittest.TestCase):
    def get_rpal_st(self, filename):
        """ Helper function to run the RPAL parser with the -st flag """
        result = subprocess.run(['python', './myrpal.py', '-st', filename], capture_output=True, text=True)
        return result.stdout.strip()

    def test_st_generation(self):
        """ Test the AST generation against expected output files """
        
        test_files = [
            ("tests/st/add", "tests/st/add.st"),
            ("tests/st/fact3", "tests/st/fact3.st"),
        ]

        for input_file, expected_file in test_files:
            # check if input file exists
            with self.subTest(input_file=input_file):
                with open(expected_file) as file:
                    expected_output = file.read().strip()
                    ast_output = self.get_rpal_st(input_file)
                    self.assertEqual(ast_output, expected_output)
