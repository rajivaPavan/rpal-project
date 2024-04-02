from .parser import Parser
from .tokens import *
class RPALParser(Parser):
    def __init__(self,src):
        super().__init__(src)
    
    __FIRST_RN = [IdentifierToken, IntegerToken, StringToken, LParenToken]
    __FIRST_VB = [IdentifierToken, LParenToken]
    
    def proc_E(self):
        if self.nextToken() != None and self.nextToken().isValue("let"):
            self.read(IdentifierToken.fromValue("let"))
            self.proc_D()
            self.read(IdentifierToken.fromValue("in"))
            self.proc_E()
            self.buildTree("let", 2)
        elif self.nextToken().isValue("fn"):
            self.read(IdentifierToken.fromValue("fn"))
            N = 1
            while (self.nextToken() != None 
                   and self.nextToken().__class__ in RPALParser.__FIRST_VB):
                self.proc_Vb()
                N += 1
            self.read(IdentifierToken.fromValue("."))
            self.proc_E()
            self.buildTree("lambda", N+1)
        else: 
            self.proc_Ew()
                            
    def proc_Ew(self):
        self.proc_T()
        if self.nextToken() != None and self.nextToken().isValue("where"):
            self.read(IdentifierToken.fromValue("where"))
            self.proc_Dr()
            self.buildTree("where", 2)
        else:
            raise InvalidTokenException.fromToken(self.nextToken())
        
    def proc_T(self):
        self.proc_Ta()
        if self.nextToken().isValue(","):
            while self.nextToken != None and self.nextToken().isValue(","):
                self.read(CommaToken.instance())
                self.proc_Ta()
                self.buildTree("tau", 2)
        else:
            raise InvalidTokenException.fromToken(self.nextToken())

    def proc_Ta(self):
        self.proc_Tc()
        while self.nextToken() != None and self.nextToken().isValue("aug"):
            self.read(IdentifierToken.fromValue("aug"))
            self.proc_Tc()
            self.buildTree("aug", 2)        
        
    def proc_Tc(self):
        self.proc_B()
        if self.nextToken().isValue("->"):
            self.read(OperatorToken.fromValue("->"))
            self.proc_Tc()
            self.read(OperatorToken.fromValue("|"))
            self.proc_Tc()
            self.buildTree("->", 3)
        else:
            raise InvalidTokenException.fromToken(self.nextToken())

    def proc_B(self):
        self.proc_Bt()
        while self.nextToken() != None and self.nextToken().isValue("or"):
            self.read(IdentifierToken.fromValue("or"))
            self.proc_Bt()
            self.buildTree("or", 2)

    def proc_Bt(self):
        self.proc_Bs()
        while self.nextToken() != None and self.nextToken().isValue("&"):
            self.read(OperatorToken.fromValue("&"))
            self.proc_Bs()
            self.buildTree("&", 2)

    def proc_Bs(self):
        if self.nextToken().isValue("not"):
            self.read(IdentifierToken.fromValue("not"))
            self.proc_Bp()
            self.buildTree("not", 1)
        else:
            self.proc_Bp()
    
    def proc_Bp(self):
        self.proc_A()
        if self.nextToken().isValue("gr"):
            self.read(IdentifierToken.fromValue("gr"))
            self.proc_A()
            self.buildTree("gr", 2)
        elif self.nextToken().isValue(">"):
            self.read(OperatorToken.fromValue(">"))
            self.proc_A()
            self.buildTree("gr", 2)
        elif self.nextToken().isValue("ge"):
            self.read(IdentifierToken.fromValue("ge"))
            self.proc_A()
            self.buildTree("ge", 2)
        elif self.nextToken().isValue(">="):
            self.read(OperatorToken.fromValue(">="))
            self.proc_A()
            self.buildTree("ge", 2)
        elif self.nextToken().isValue("ls"):
            self.read(IdentifierToken.fromValue("ls"))
            self.proc_A()
            self.buildTree("ls", 2)
        elif self.nextToken().isValue("<"):
            self.read(OperatorToken.fromValue("<"))
            self.proc_A()
            self.buildTree("ls", 2)
        elif self.nextToken().isValue("le"):
            self.read(IdentifierToken.fromValue("le"))
            self.proc_A()
            self.buildTree("le", 2)
        elif self.nextToken().isValue("<="):
            self.read(OperatorToken.fromValue("<="))
            self.proc_A()
            self.buildTree("le", 2)
        elif self.nextToken().isValue("eq"):
            self.read(IdentifierToken.fromValue("eq"))
            self.proc_A()
            self.buildTree("eq", 2)
        elif self.nextToken().isValue("ne"):
            self.read(IdentifierToken.fromValue("ne"))
            self.proc_A()
            self.buildTree("ne", 2)
        elif self.nextToken().isValue(";"):
            self.read(SemiColonToken.instance())
        else:
            raise InvalidTokenException.fromToken(self.nextToken())

    def proc_A(self):
        # A -> (At; | +At | -At) ( ('+' At) | ('-' At) )+
        if self.nextToken().__class__ == OperatorToken:
            if self.nextToken().isValue("+"):
                self.read(OperatorToken.fromValue("+"))
                self.proc_At()
            elif self.nextToken().isValue("-"):
                self.read(OperatorToken.fromValue("-"))
                self.proc_At()
                self.buildTree("neg", 1)
            else:
                raise InvalidTokenException.fromToken(self.nextToken())
        # SELECT(At) = FIRST(Rn)
        elif self.nextToken().__class__ in RPALParser.__FIRST_RN: 
            self.proc_At()
        else:
            raise InvalidTokenException.fromToken(self.nextToken())
        
        while(self.nextToken() != None and 
              self.nextToken().__class__ == OperatorToken
              and (self.nextToken().isValue("+") or self.nextToken().isValue("-"))):
            if self.nextToken().isValue("+"):
                self.read(OperatorToken.fromValue("+"))
                self.proc_At()
                self.buildTree("+", 2)
            else:
                self.read(OperatorToken.fromValue("-"))
                self.proc_At()
                self.buildTree("-", 2)

    def proc_At(self):
        
        self.proc_Af()
        
        _next_token = self.nextToken()
        while ( _next_token != None and 
               _next_token.__class__ == OperatorToken 
            and (_next_token.isValue("*")) or _next_token.isValue("/")):
        
            # read the operator token and build the tree using the appropriate transduction rule
            if _next_token.isValue("*"):
                self.read(OperatorToken.fromValue("*"))
                self.proc_Af()
                self.buildTree("*", 2)
            else:
                self.read(OperatorToken.fromValue("/"))
                self.proc_Af()
                self.buildTree("/", 2)
            # update the next token
            _next_token = self.nextToken()

    def proc_Af(self):
        
        self.proc_Ap()
        if self.nextToken().isValue("**"):
            self.read(OperatorToken.fromValue("**"), ignore=True)
            self.proc_Af()
            self.buildTree("**", 2)
        else:
            raise InvalidTokenException.fromToken(self.nextToken())
        
    def proc_Ap(self):
                
        self.proc_R()
            
        # check if the next token is a @ 
        while self.nextToken() != None and self.nextToken().isValue("@"):
            # read the @ token and ignore it
            self.read(OperatorToken.fromValue("@"))
            
            # next token should be an identifier
            self.read(IdentifierToken.fromValue(self.nextToken().value))
            
            self.proc_R()
            self.buildTree("@", 3)

    def proc_R(self):
        self.proc_Rn()
        n = 1
        while (self.nextToken() != None 
               and self.nextToken().__class__ in RPALParser.__FIRST_RN):
            self.proc_Rn()
            n += 1
        self.buildTree("gamma", n)
        
        
    def proc_Rn(self):
        
        token = self.nextToken()
        
        if token.__class__ == IdentifierToken:
            # read the identifier token
            self.read(token, ignore=False)
            if token.value in ["true", "false", "nil", "dummy"]:
                # build the tree with the token value
                self.buildTree(token.value, 0)
        elif token.__class__ in [IntegerToken, StringToken]:
            # read the integer or string token
            self.read(token, ignore = False)
            
        elif token.__class__ == LParenToken:
            # read and ignore the ( token
            self.read(token)
            self.proc_E()
            # read and ignore the ) token
            self.read(RParenToken.instance())
        else:
            raise Exception("Invalid token: Identifier, Integer, String or \"(\" expected but found: " + str(token))


    def proc_D(self):
        self.proc_Da()
        if self.nextToken().isValue("within"):
            self.read(IdentifierToken.fromValue("within"))
            self.proc_D()
            self.buildTree("within", 2)
        
    def proc_Da(self):
        self.proc_Dr()
        while self.nextToken() != None and self.nextToken().isValue("and"):
            self.read(IdentifierToken.fromValue("and"))      
            self.proc_Dr()
            self.buildTree("and", 2)
        
    
    def proc_Dr(self):
        if self.nextToken().isValue("rec"):
            self.read(IdentifierToken.fromValue("rec"))
            self.proc_Db()
            self.buildTree("rec", 1)
        else:
            self.proc_Db()
        
        
    def proc_Db(self):
        
        token = self.nextToken()    
        if(token.__class__ == LParenToken):
            self.read(LParenToken.instance())
            self.proc_D()
            self.read(RParenToken.instance())
        elif(token.__class__ == IdentifierToken):
            look_ahead = self.lookahead()
            if look_ahead != None and look_ahead.__class__ == CommaToken:
                self.proc_Vl()
                self.read(OperatorToken.fromValue("="))
                self.proc_E()
                self.buildTree("=", 2)
            elif look_ahead != None and look_ahead.__class__ in RPALParser.__FIRST_VB:
                self.read(IdentifierToken.fromValue(self.nextToken().value))
                N = 1
                while(self.nextToken() != None 
                and self.nextToken().__class__ in RPALParser.__FIRST_VB):
                    self.proc_Vb()
                    N += 1
                self.read(OperatorToken.fromValue("="))
                self.proc_E()
                self.buildTree("fcn_form", N+2)
            else:
                raise InvalidTokenException.fromToken(token)
        else:
            raise InvalidTokenException.fromToken(token)

             
    def proc_Vb(self):
        token = self.nextToken()
        if(token.__class__ == IdentifierToken):
            self.read(self.nextToken(), ignore = False)
        elif(token.__class__ == LParenToken):
            self.read(LParenToken.instance())
            if(self.nextToken().__class__ == RParenToken):
                self.read(RParenToken.instance())
                self.buildTree("()", 0)
            else:
                self.proc_Vl()
                self.read(RParenToken.instance())
        else:
            raise InvalidTokenException.fromToken(token)
        
    def proc_Vl(self):
        self.read(IdentifierToken.fromValue(self.nextToken().value), ignore = False)
        if (self.nextToken() != None and self.nextToken().__class__ != CommaToken):
            raise InvalidTokenException.fromToken(self.nextToken())
        N = 1
        while(self.nextToken() != None and self.nextToken().__class__ != CommaToken):
            self.read(CommaToken.instance())
            self.read(IdentifierToken.fromValue(self.nextToken().value), ignore = False)
            N += 1
        self.buildTree(",", N)
            
    def parse(self):
            """Parses the source program and returns the Abstract Syntax Tree (AST).

            Returns:
                The Abstract Syntax Tree (AST) of the source program.
            """
            self.proc_E()
            return self.getAST()
    
