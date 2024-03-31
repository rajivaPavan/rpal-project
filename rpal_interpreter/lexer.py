import re
from .tokens import *

class Lexer:
    def __init__(self, program):
        self.program = program
        self.tokens = []
        self.position = 0
        self.line_no = 1
        self.char_pos = 1
        
    def reset(self):
        self.tokens = []
        self.position = 0
        self.line_no = 1
        self.char_pos = 1

    def tokenize(self, count = -1):
        counter = 0
        while self.position < len(self.program):
            self.nextToken()
            counter+=1
            if counter == count:
                break
            
        return self.tokens
            
    def nextToken(self):
        token = None
        while token == None and self.position < len(self.program):
            token = self.__nextToken()
        return token 
    
    def __nextToken(self):
        """
        Retrieves the next token from the program string.

        Returns:
            str: The next token from the program string.

        Raises:
            InvalidTokenException: If the next token is invalid.
        """
        program = self.program
        position = self.position
        
        if position >= len(program):
            return None
        
        tokens = self.tokens
        line_no = self.line_no
        char_pos = self.char_pos

        # using re get the first token that matches the pattern and the position at which it ends
        match = None
        res = None
        
        # the order of the token types is important as some tokens are substrings of others
        for token_type in [CommentToken, SpacesToken, IdentifierToken,
                               IntegerToken, StringToken, OperatorToken, 
                               LParenToken, RParenToken, SemiColonToken, CommaToken]:
            regex = token_type.regex()
            match = regex.match(program, position)
            if not(match):
                continue

            # get the matched token
            token_val = match.group(0)
            position = match.end()
            char_pos += len(token_val)
            
            # update line number if token is comment or spaces and ignore them
            if token_type == CommentToken or token_type == SpacesToken:
                newlines = token_val.count("\n")
                if newlines > 0:
                    char_pos = 1 # reset char position to 1
                    line_no += newlines
                break
                            
            # punctions have no arguments in their constructor
            if (token_type == LParenToken 
                or token_type == RParenToken 
                or token_type == SemiColonToken 
                or token_type == CommaToken):
                    res = token_type(line_no, char_pos)
                    tokens.append(res)
            else:
                res = token_type(token_val, line_no, char_pos)
                tokens.append(res)
                   
            break         
            
        if not match:   
            raise InvalidTokenException(line_no, char_pos)
                
        # update the position, line number and character position
        self.position = position
        self.line_no = line_no
        self.char_pos = char_pos
        
        return res