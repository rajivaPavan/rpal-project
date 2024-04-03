import re

class TokenRegex:
    OPERATOR_SYMBOL ="+\-*<>&.@/:=~|$!#%^_\[\]\{\}\"\'?"
    Identifier = re.compile(r"[a-zA-Z][a-zA-Z0-9_]*")
    Integer = re.compile(r"[0-9]+")
    Operator = re.compile(r"[+\-*<>&.@/:=~|$!#%^_\[\]\{\}\"\'?]+")
    String = re.compile(r"\"[(\\t)(\\n)(\\)(\\\")\(\);,\sa-zA-Z0-9+\-*<>&.@/:=~|$!#%^_\[\]\{\}\"\'?]*\"")
    Spaces = re.compile(r"[\s\n]+")
    Comment = re.compile(r"\/\/[\"\(\);,\\ a-zA-Z0-9+\-*<>&.@/:=~|$!#%^_\[\]\{\}\"\'?]*\n")
    OpenParen = re.compile(r"\(")
    CloseParen = re.compile(r"\)")
    SemiColon = re.compile(r";")
    Comma = re.compile(r",")
    
class Token:
    """
    Represents a token in the interpreter.

    Attributes:
        type (str): The type of the token.
        value (str): The value of the token.
        line (int): The line number where the token appears.
        col (int): The column number where the token appears.
    """

    def __init__(self, type, value, line = None, col = None):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"({self.type}, {repr(self.value)})"

    def regex():
        raise NotImplementedError("regex method not implemented")
    
    def isType(self, t):
        return self.__class__ == t
    
    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.type == other.type and self.value == other.value
    
    def isValue(self, value):
        return self.value == value
    
    @classmethod
    def fromValue(cls, value):
        return cls(value, None, None)
    
    @classmethod
    def instance(cls):
        return cls(None, None)
    
    
class IdentifierToken(Token):
    def __init__(self, value, line, col):
        super().__init__("<IDENTIFIER>", value, line, col)
        
    def regex():
        return TokenRegex.Identifier
    
    def __str__(self):
        return f"<ID:{self.value}>"
    
        
class IntegerToken(Token):
    def __init__(self, value, line, col):
        super().__init__("<INTEGER>", value, line, col)
        
    def regex():
        return TokenRegex.Integer
    
    def __str__(self):
        return f"<INT:{self.value}>"
    
    
class OperatorToken(Token):      
    def __init__(self, value, line, col):
        super().__init__("<OPERATOR>", value, line, col)
    
    def regex():
        return TokenRegex.Operator
        
class StringToken(Token):
    def __init__(self, value, line, col):
        super().__init__("<STRING>", value, line, col)
        
    def regex():
        return TokenRegex.String
    
    def __str__(self):
        return f"<STR:{self.value}>"
    
    
class SpacesToken(Token):
    def __init__(self, line, col):
        super().__init__("<DELETE>", None, line, col)
        
    def regex():
        return TokenRegex.Spaces

class CommentToken(Token):
    def __init__(self, line, col):
        super().__init__("<DELETE>", None, line, col)
        
    def regex():
        return TokenRegex.Comment
    
class LParenToken(Token):
    """Represents a left parenthesis token."""

    def __init__(self, line, col):
        super().__init__("(", None, line, col)
    
    def regex():
        return TokenRegex.OpenParen
    
    
class RParenToken(Token):
    """
    Represents a right parenthesis token in the RPAL interpreter.
    """
    def __init__(self, line, col):
        super().__init__(")", None, line, col)
    
    def regex():
        return TokenRegex.CloseParen
    
class SemiColonToken(Token):
    """
    Represents a semicolon token in the interpreter.
    """
    def __init__(self, line, col):
        super().__init__(";", None, line, col)
    
    def regex():
        return TokenRegex.SemiColon
    
class CommaToken(Token):
    """
    Represents a comma token in the RPAL language.
    """
    def __init__(self, line, col):
        super().__init__(",", None, line, col)
        
    def regex():
        return TokenRegex.Comma


class InvalidTokenException(Exception):
        
    @classmethod
    def fromToken(cls, token:Token):
        return cls(f"Invalid token: {token.value} at line {token.line}, col {token.col}")
    
    @classmethod
    def fromLine(cls, line, col):
        return cls(f"Invalid token at line {line}, char {col}")
    