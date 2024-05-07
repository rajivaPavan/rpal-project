class DefinedFunctions:
    PRINT = "Print"
    ORDER = "Order"
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
            DefinedFunctions.ISINTEGER,
            DefinedFunctions.ISSTRING,
            DefinedFunctions.ISTRUTHVALUE,
            DefinedFunctions.ISTUPLE,
            DefinedFunctions.ISFUNCTION,
            DefinedFunctions.ISDUMMY
        ]

    def isdefined(name):
        return name in DefinedFunctions.get_functions()
    


class DefinedFunction():
    """"""
    def __init__(self, __name):
        self.__name = __name

    def run(self, arg):
        raise NotImplementedError
    
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
        else:
            raise Exception(f"Invalid function name: {name}")
    
class PrintFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.PRINT)
    
    def run(self, arg):
        print(arg)

class OrderFn(DefinedFunction):
    def __init__(self):
        super().__init__(DefinedFunctions.ORDER)
    
    def run(self, arg):
        return len(arg)

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
