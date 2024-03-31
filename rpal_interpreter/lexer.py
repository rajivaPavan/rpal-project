import re
from .tokens import *

class Lexer:

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

            # using re get the first token that matches the pattern and the position at which it ends
            match = None
            for token_type in Token.__subclasses__():
                regex = token_type.regex()
                match = regex.match(program, position)
                if not(match):
                    continue

                # get the matched token
                token = match.group(0)
                position = match.end()
                
                # ignore spaces and comments
                if token_type == CommentToken or token_type == SpacesToken:
                    break
                                
                # punctions have no arguments in their constructor
                if (token_type == LParenToken 
                    or token_type == RParenToken 
                    or token_type == SemiColonToken 
                    or token_type == CommaToken):
                    tokens.append(token_type())
                else:
                    tokens.append(token_type(token))
                       
                break         
                
            if not match:   
                raise Exception(f"Invalid token at position {position}")
                
        return tokens