class Nodes:
    # reserved AST node values
    LET = "let"
    LAMBDA = "lambda"
    TAU = "tau"
    AUG = "aug"
    COND = "->"
    WHERE = "where"
    OR = "or"
    AND_OP = "&"
    NOT = "not"
    GR = "gr"
    GE = "ge"
    LS = "ls"
    LE = "le"
    EQ = "eq"
    NE = "ne"
    PLUS = "+"
    MINUS = "-"
    NEG = "neg"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "**"
    AT = "@"
    GAMMA = "gamma"
    TRUE = "true"
    FALSE = "false"
    NIL = "nil"
    DUMMY = "dummy"
    WITHIN = "within"
    AND = "and"
    REC = "rec"
    ASSIGN = "="
    FCN_FORM = "fcn_form"
    PARENS = "()"
    COMMA = ","
    YSTAR = "<Y*>"

    UOP = [NEG, NOT]
    BOP = [AUG, OR, AND_OP, GR, GE, LS, LE, EQ, NE, PLUS, MINUS, MULTIPLY, DIVIDE, POWER]