class DefinedFunctions:
    PRINT = "Print"
    ORDER = "Order"
    CONC = "Conc"
    STEM = "Stem"
    STERN = "Stern"
    ISINTEGER = "Isinteger"
    ISSTRING = "Isstring"
    ISTRUTHVALUE = "Istruthvalue"
    ISTUPLE = "Istuple"
    ISFUNCTION = "Isfunction"
    ISDUMMY = "Isdummy"

    @staticmethod
    def get_functions():
        return [
            DefinedFunctions.PRINT,
            DefinedFunctions.ORDER,
            DefinedFunctions.CONC,
            DefinedFunctions.STEM,
            DefinedFunctions.STERN,
            DefinedFunctions.ISINTEGER,
            DefinedFunctions.ISSTRING,
            DefinedFunctions.ISTRUTHVALUE,
            DefinedFunctions.ISTUPLE,
            DefinedFunctions.ISFUNCTION,
            DefinedFunctions.ISDUMMY,
        ]

    def isdefined(name):
        return name in DefinedFunctions.get_functions()
    


class DefinedFunction():
    """"""
    def __init__(self, __name):
        self.__name = __name

    def run(self, arg):
        raise NotImplementedError
    
    def getName(self):
        return self.__name
    
    def __repr__(self):
        return f"fn: {self.__name}"
    

class FunctionFactory:
    @staticmethod
    def create(name):
        if name == DefinedFunctions.PRINT:
            return PrintFn()
        elif name == DefinedFunctions.ORDER:
            return OrderFn()
        elif name == DefinedFunctions.ISINTEGER:
            return IsIntegerFn()
        elif name == DefinedFunctions.ISSTRING:
            return IsStringFn()
        elif name == DefinedFunctions.ISTRUTHVALUE:
            return IsTruthValueFn()
        elif name == DefinedFunctions.ISTUPLE:
            return IsTupleFn()
        elif name == DefinedFunctions.ISFUNCTION:
            return IsFunctionFn()
        elif name == DefinedFunctions.ISDUMMY:
            return IsDummyFn()
        elif name == DefinedFunctions.CONC:
            return ConcFn()
        elif name == DefinedFunctions.STEM:
            return StemFn()
        elif name == DefinedFunctions.STERN:
            return SternFn()
        else:
            raise Exception(f"Invalid function name: {name}")
    
class PrintFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.PRINT)
    
    def run(self, arg):
        # strip ' in the beginning and end
        arg = PrintFn.__handler(arg)
        print(arg)

    @staticmethod
    def __handler(arg):
        if isinstance(arg, str):
            # replace \n with newline
            arg = arg.replace("\\n", "\n")
            return arg.strip("'")
        elif isinstance(arg, bool):
            return "true" if arg else "false"
        elif isinstance(arg, tuple):
            tuple_ = str(arg)
            tuple_ = tuple_.lstrip("(").rstrip(")")
            tuple_ = tuple_.rstrip(",")
            return f"({tuple_})"
        return arg

class OrderFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ORDER)
    
    def run(self, arg):
        return len(arg)

class ConcFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.CONC)
    
    def run(self, args):
        # strip ' in the beginning and end
        args = [arg.strip("'") for arg in args]
        # concatenate the strings
        res = "".join(args)
        return f"'{res}'"
        

class StemFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.STEM)
    
    def run(self, arg):
        return arg[0]
    
class SternFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.STERN)
    
    def run(self, arg):
        return arg[-1]

class IsIntegerFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ISINTEGER)
    
    def run(self, arg):
        return isinstance(arg, int)

class IsStringFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ISSTRING)
    
    def run(self, arg):
        return isinstance(arg, str)
    
class IsTruthValueFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ISTRUTHVALUE)
    
    def run(self, arg):
        return isinstance(arg, bool)
    
class IsTupleFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ISTUPLE)
    
    def run(self, arg):
        
        return isinstance(arg, tuple)
    
class IsFunctionFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ISFUNCTION)
    
    def run(self, arg):
        raise NotImplementedError
    
class IsDummyFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ISDUMMY)
    
    def run(self, arg):
        return arg == "dummy"
