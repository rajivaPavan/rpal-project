import re
from .tokens import *
import queue as q

class Lexer:
    """
    The Lexer class is responsible for tokenizing a program string into a list of tokens.

    Attributes:
        program (str): The program string to be tokenized.
        tokens (list): The list of tokens generated from the program string.
        position (int): The current position in the program string.
        line_no (int): The current line number.
        char_pos (int): The current character position.

    Methods:
        reset(): Resets the lexer to its initial state.
        tokenize(count=-1): Tokenizes the program string up to a specified count.
        nextToken(): Retrieves the next token from the program string.
        __nextToken(): Retrieves the next token from the program string (internal method).

    Raises:
        InvalidTokenException: If the next token is invalid.
    """

    def __init__(self, program):
        self.__program = program
        self.__position = 0
        self.__line_no = 1
        self.__char_pos = 1
        self.__look_ahead_q = q.Queue()
        
    def reset(self):
        """
        Resets the lexer to its initial state.
        """
        self.__position = 0
        self.__line_no = 1
        self.__char_pos = 1

    def lookAhead(self):
        """
        Retrieves the next token from the program string without consuming the token
        
        Returns: Next Token or None if there are no more tokens.
        """
        if self.__look_ahead_q.empty():
            tokens = self.tokenize(count=1)
            if len(tokens) == 0:
                return None
            else:
                self.__look_ahead_q.put(tokens[0])
                return tokens[0]
        else:
            return self.__look_ahead_q.queue[0]
            
    
    def nextToken(self):
        """
        Retrieves the next token from the program string. This consumes the token. 
        Returns only if there are no more tokens.
        
        Returns:
            Token: The next token from the program string | None if there are no more tokens.
        """        

        if not self.__isScanning():
            return None
        
        if self.__look_ahead_q.empty():
            self.__tokenize()
               
        try:
            t = self.__look_ahead_q.get(block=False) 
        except q.Empty:
            t = None
        return t

    def tokenize(self, count:int=-1):
        """
        Tokenizes the program string up to a specified count and 
        returns the list of tokens from the look ahead queue.

        Args:
            count (int, optional): The number of tokens to tokenize. Defaults to -1.

        Returns:
            list: The list of tokens generated from the program string.
        """
        tokens = []
        self.__tokenize(count)
        while not self.__look_ahead_q.empty():
            tokens.append(self.__look_ahead_q.get())
        return tokens

    def __tokenize(self, count:int=1):
        """
        Tokenizes the program by extracting tokens using the __lexToken method.
        This method adds the tokens to the look ahead queue.

        Args:
            count (int, optional): The number of tokens to tokenize. Defaults to 1.

        Returns:
            None

        """
        counter = 0
        while self.__isScanning():
            token = self.__lexToken()
            if token == None:
                break
            self.__look_ahead_q.put(token)
            counter += 1
            if counter == count:
                break

    def __isScanning(self):
        return self.__position < len(self.__program)
            
                    
    def __lexToken(self):
        """
        Lexes the next token in the program.

        Returns:
            The next token in the program, or None if there are no more tokens.
        """
        token = None
        while token == None and self.__isScanning():
            token = self.__lex()
        return token
    
    def __lex(self):
        """
        Retrieves the next token from the program string.

        Returns:
            Token: The next token from the program string. 
            Can be None if no token is a <DELETE> token or if end of program is reached.

        Raises:
            InvalidTokenException: If the next token is invalid.
        """
        program = self.__program
        position = self.__position
        
        if position >= len(program):
            return None
        
        line_no = self.__line_no
        char_pos = self.__char_pos

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
            
            # update line number if token has newlines - this includes CommentTokens and SpaceTokens with \n
            if '\n' in token_val:
                line_no += token_val.count('\n')
                char_pos = 1 # reset character position
                break
            
            # count spaces and tabs
            if token_type == SpacesToken:
                char_pos += len(token_val)
                break
                            
            # punctions have no arguments in their constructor
            if (token_type == LParenToken 
                or token_type == RParenToken 
                or token_type == SemiColonToken 
                or token_type == CommaToken):
                    res = token_type(line_no, char_pos)
            else:
                if token_val in KeywordToken.values():
                    res = KeywordToken(token_val, line_no, char_pos)
                else:
                    res = token_type(token_val, line_no, char_pos)     

            char_pos += len(token_val)
            break         
            
        if not match:   
            raise InvalidTokenException.fromLine(line_no, char_pos)
                
        
        # update the position, line number and character position
        self.__position = position
        self.__line_no = line_no
        self.__char_pos = char_pos
        
        return res