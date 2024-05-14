

class DefinedFunctions:
    """The functions defined in the Primitive Environment are represented here."""
    
    PRINT = "Print"
    ORDER = "Order"
    CONC = "Conc"
    STEM = "Stem"
    STERN = "Stern"
    ITOS = "ItoS"
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
            DefinedFunctions.ITOS,
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
    """A parent class for the defined functions in the Primitive Environment."""
    
    def __init__(self, __name):
        self.__name = __name

    def run(self, arg):
        raise Exception("Abstract method run() not implemented.")
    
    def getName(self):
        return self.__name
    
    def __repr__(self):
        return f"fn: {self.__name}"
    

class FunctionFactory:
    """A factory class to create objects to define the functions of each predefined function."""
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
        elif name == DefinedFunctions.ITOS:
            return ItoSFn()
        else:
            raise Exception(f"Invalid function name: {name}")
    
class PrintFn(DefinedFunction):
    """The Print function in the Primitive Environment."""
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
            return arg
        elif isinstance(arg, bool):
            return "true" if arg else "false"
        elif isinstance(arg, tuple):
            tuple_ = str(arg)
            tuple_ = tuple_.lstrip("(").rstrip(")")
            tuple_ = tuple_.rstrip(",")
            return f"({tuple_})"
        return arg

class OrderFn(DefinedFunction):
    """The Order function in the Primitive Environment.
    Returns the length of tuple"""
    def __init__(self):
        super().__init__(DefinedFunctions.ORDER)
    
    def run(self, arg):
        return len(arg)

class ConcFn(DefinedFunction):
    """The Concatenate function in the Primitive Environment.
    Concatenates the strings in the tuple"""
    def __init__(self):
        super().__init__(DefinedFunctions.CONC)
    
    def run(self, args):
        args = [arg for arg in args]
        # concatenate the strings
        res = "".join(args)
        return res
        

class StemFn(DefinedFunction):
    """The Stem function in the Primitive Environment.
    Returns the first character of the string."""
    def __init__(self):
        super().__init__(DefinedFunctions.STEM)
    
    def run(self, arg):
        if type(arg) != str:
            raise Exception("Stem can only be applied to strings")
        
        stem = arg[0] if len(arg) > 0 else ""
        return stem
    
class SternFn(DefinedFunction):
    """The Stern function in the Primitive Environment.
    Returns the string without the first character."""
    def __init__(self):
        super().__init__(DefinedFunctions.STERN)
    
    def run(self, arg):
        if type(arg) != str:
            raise Exception("Stern can only be applied to strings")
        return arg[1:] if len(arg) > 0 else ""
    
class ItoSFn(DefinedFunction):
    """The ItoS function in the Primitive Environment.
    Converts the integer to string."""
    def __init__(self):
        super().__init__(DefinedFunctions.ITOS)
    
    def run(self, arg):
        if not isinstance(arg, int):
            raise Exception("ItoS can only be applied to integers")
        return str(arg)

class IsIntegerFn(DefinedFunction):
    """The IsInteger function in the Primitive Environment.
    Checks if the argument is an integer."""
    def __init__(self):
        super().__init__(DefinedFunctions.ISINTEGER)
    
    def run(self, arg):
        return isinstance(arg, int)

class IsStringFn(DefinedFunction):
    """The IsString function in the Primitive Environment.
    Checks if the argument is a string."""
    def __init__(self):
        super().__init__(DefinedFunctions.ISSTRING)
    
    def run(self, arg):
        return isinstance(arg, str)
    
class IsTruthValueFn(DefinedFunction):
    """The IsTruthValue function in the Primitive Environment.
    Checks if the argument is a boolean value."""
    def __init__(self):
        super().__init__(DefinedFunctions.ISTRUTHVALUE)
    
    def run(self, arg):
        return isinstance(arg, bool)
    
class IsTupleFn(DefinedFunction):
    """The IsTuple function in the Primitive Environment.
    Checks if the argument is a tuple."""
    def __init__(self):
        super().__init__(DefinedFunctions.ISTUPLE)
    
    def run(self, arg):
        is_tuple =  isinstance(arg, tuple)
        return is_tuple
    
class IsFunctionFn(DefinedFunction):
    """The IsFunction function in the Primitive Environment.
    Checks if the argument is a function."""
    def __init__(self):
        super().__init__(DefinedFunctions.ISFUNCTION)
    
    def run(self, arg):
        raise NotImplementedError
    
class IsDummyFn(DefinedFunction):
    """The IsDummy function in the Primitive Environment.
    Checks if the argument is a dummy value."""
    def __init__(self):
        super().__init__(DefinedFunctions.ISDUMMY)
    
    def run(self, arg):
        return arg == "dummy"
