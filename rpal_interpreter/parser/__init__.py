class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        return self.expr()

    def eat(self, token_type):
        if self.position < len(self.tokens) and self.tokens[self.position][0] == token_type:
            current_token = self.tokens[self.position]
            self.position += 1
            return current_token
        else:
            raise Exception(f"Expected token type {token_type}, but got {self.tokens[self.position][0]}")

    def expr(self):
        """expr -> term ((PLUS | MINUS) term)*"""
        node = self.term()

        while self.position < len(self.tokens) and self.tokens[self.position][0] in ('OPERATOR',) and self.tokens[self.position][1] in ('+', '-'):
            op = self.tokens[self.position]
            self.eat('OPERATOR')
            node = ('BINOP', op, node, self.term())

        return node

    def term(self):
        """term -> factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.position < len(self.tokens) and self.tokens[self.position][0] in ('OPERATOR',) and self.tokens[self.position][1] in ('*', '/'):
            op = self.tokens[self.position]
            self.eat('OPERATOR')
            node = ('BINOP', op, node, self.factor())

        return node

    def factor(self):
        """factor -> NUMBER | LPAREN expr RPAREN"""
        token = self.tokens[self.position]

        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ('NUMBER', token[1])
        elif token[0] == 'PARENTHESIS' and token[1] == '(':
            self.eat('PARENTHESIS')
            node = self.expr()
            self.eat('PARENTHESIS')
            return node
        else:
            raise Exception(f"Unexpected token: {token}")