class Lexer:
    def __init__(self):
        # Initialize any necessary variables, token definitions, etc.
        self.token_types = {
            'WHITESPACE': ' \t\n',
            'NUMBERS': '0123456789',
            'LETTERS': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'OPERATORS': '+-*/=',
            'PARENTHESIS': '()',
        }

    def lex(self, program):
        """
        Converts a string of program code into a list of tokens.

        Args:
            program (str): The source code as a string.

        Returns:
            list: A list of tokens extracted from the source code.
        """
        tokens = []
        position = 0

        while position < len(program):
            char = program[position]

            if char in self.token_types['NUMBERS']:
                number = char
                while position + 1 < len(program) and program[position + 1] in self.token_types['NUMBERS']:
                    position += 1
                    number += program[position]
                tokens.append(('NUMBER', number))

            elif char in self.token_types['LETTERS']:
                identifier = char
                while position + 1 < len(program) and program[position + 1] in self.token_types['LETTERS'] + self.token_types['NUMBERS']:
                    position += 1
                    identifier += program[position]
                tokens.append(('IDENTIFIER', identifier))

            elif char in self.token_types['OPERATORS']:
                tokens.append(('OPERATOR', char))

            elif char in self.token_types['WHITESPACE']:
                pass

            elif char in self.token_types['PARENTHESIS']:
                tokens.append(('PARENTHESIS', char))
            
            else:
                print(f"Unknown character: {char}")

            position += 1

        return tokens
