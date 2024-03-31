import re

class TokenRegex:
    OPERATOR_SYMBOL ="+\-*<>&.@/:=~|$!#%^_\[\]\{\}\"\'?"
    Identifier = re.compile(r"[a-zA-Z][a-zA-Z0-9_]*")
    Integer = re.compile(r"[0-9]+")
    Operator = re.compile(r"["+OPERATOR_SYMBOL+"]+")
    String = re.compile(r"\"[(\\t)(\\n)(\\)(\\\")\(\);,\sa-zA-Z0-9"+OPERATOR_SYMBOL+"]*\"")
    Spaces = re.compile(r"[\s\n]+")
    Comment = re.compile(r"//[\"\(\);,\\ a-zA-Z0-9"+OPERATOR_SYMBOL+"]*\n")
    OpenParen = re.compile(r"\(")
    CloseParen = re.compile(r"\)")
    SemiColon = re.compile(r";")
    Comma = re.compile(r",")
    
class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"({self.type}, {repr(self.value)})"
    
    def regex():
        raise NotImplementedError("regex method not implemented")
    
    
class IdentifierToken(Token):
    def __init__(self, value, line, col):
        super().__init__("<IDENTIFIER>", value, line, col)
        
    def regex():
        return TokenRegex.Identifier
    
        
class IntegerToken(Token):
    def __init__(self, value, line, col):
        super().__init__("<INTEGER>", value, line, col)
        
    def regex():
        return TokenRegex.Integer
    
    
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
    def __init__(self, line, col):
        super().__init__("(", None, line, col)
    
    def regex():
        return TokenRegex.OpenParen
    
    
class RParenToken(Token):
    def __init__(self, line, col):
        super().__init__(")", None, line, col)
    
    def regex():
        return TokenRegex.CloseParen
    
class SemiColonToken(Token):
    def __init__(self, line, col):
        super().__init__(";", None, line, col)
    
    def regex():
        return TokenRegex.SemiColon
    
class CommaToken(Token):
    def __init__(self, line, col):
        super().__init__(",", None, line, col)
        
    def regex():
        return TokenRegex.Comma


class InvalidTokenException(Exception):
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def __str__(self):
        return f"Invalid token at line {self.line}, char {self.col}"
    