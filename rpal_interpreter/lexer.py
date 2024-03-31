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
        line_no = 1
        char_pos = 1

        while position < len(program):

            # using re get the first token that matches the pattern and the position at which it ends
            match = None
            for token_type in [CommentToken, SpacesToken, IdentifierToken,
                               IntegerToken, OperatorToken, StringToken, 
                               LParenToken, RParenToken, SemiColonToken, CommaToken]:
                regex = token_type.regex()
                match = regex.match(program, position)
                if not(match):
                    continue

                # get the matched token
                token = match.group(0)
                position = match.end()
                char_pos += len(token)
                
                # update line number if token is comment or spaces and ignore them
                if token_type == CommentToken or token_type == SpacesToken:
                    newlines = token.count("\n")
                    if newlines > 0:
                        char_pos = 1 # reset char position to 1
                        line_no += newlines
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
                raise Exception(f"Invalid token at line {line_no}, char {char_pos}")
                
        return tokens