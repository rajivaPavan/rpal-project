import pprint

from interpreter.cse_machine.functions import DefinedFunction
from .control_structures import CSInitializer
from .st import STNode
from .symbol import *
from .stack import Stack
from .environment import Environment
from .control import Control
import logger
import structs.stack as ds

class CSEMachine:
    """
    The CSEMachine class is responsible for simulating the Control Structure Environment (CSE) machine
    used in the RPAL language interpreter. It manages the control structures, environment, and stack
    to intepret the RPAL code. The class provides methods to evaluate expressions based on the cse machine rules
    """

    def __init__(self, st:STNode):
        """
        Initializes the CSE machine with the given standardized tree.
        
        Args:
        st (STNode): The standardized tree which is used to generate control structures.
        """
        # inti control
        self.csMap  = CSInitializer(st).init()
        self.control = Control(self.csMap.get(0))
        
        # init env
        self.envIndexCounter = 0
        self.envMap = dict()
        self.__envStack: ds.Stack[Environment] = ds.Stack()
        self.__create_env(self.envIndexCounter)


        # init stack
        self.stack = Stack()
        self.stack.pushStack(EnvMarkerSymbol(0)) # e0 is the first in the stack

        # set the initialized logger object
        self.logger = logger.logger
        
        self.logger.info(f"csMap: \n{self.csMap}\n")

    def __create_env(self, index, parent_index = None):
        """Creates new env and sets it as current env and adds to env to envMap"""
        parent = None
        if parent_index is not None:
            parent = self.envMap[parent_index]

        new_env = Environment(index,parent)
        self.envMap[index] = new_env
        self.__envStack.push(new_env)        

    def evaluate(self):
        
        """Evaluates the Control."""
        
        self.logger.debug(f"control {self.control}")
        self.logger.debug(f"stack {self.stack}")

        right_most = self.control.removeRightMost()

        if right_most is None:
            return

        if right_most.isType(NameSymbol) or right_most.isType(YStarSymbol):
            self.stackName(right_most)       
              
        elif right_most.isType(LambdaSymbol):
            _lambda = right_most
            self.stackLambda(_lambda)
            
        elif right_most.isType(GammaSymbol):
            top = self.stack.popStack() 
        
            if top.isType(YStarSymbol):
                # Rule 12
                self.applyYStar()
            elif top.isType(EtaClosureSymbol):
                # Rule 13
                self.applyFP(top)
            elif top.isType(NameSymbol):
                # Rule 10
                tuple_symbol:TupleSymbol = top.name
                self.tupleSelection(tuple_symbol)
            elif top.isType(LambdaClosureSymbol):
                # Rule 4, 11
                self.applyLambda(top)
            elif top.isType(FunctionSymbol):
                self.applyFunction(top)
            else: 
                raise Exception(f"Invalid symbol:{top, type(top)} in stack for gamma in Control")
                   
        elif right_most.isType(EnvMarkerSymbol):
            env_marker = right_most
            self.exitEnv(env_marker)
            
        elif right_most.isType(BinaryOperatorSymbol):
            _binop = right_most.operator
            self.binop(_binop)
            
        elif right_most.isType(UnaryOperatorSymbol):
            _unop = right_most.operator
            self.unop(_unop)
            
        elif right_most.isType(BetaSymbol):
            self.conditional()
            
        elif right_most.isType(TauSymbol):
            _tau = right_most
            self.tupleFormation(_tau)
        else:
            pass
            #TODO: throw an exception
               
        return self.evaluate()
        
    def currentEnv(self)->Environment:
        """
        Returns the current environment.
        """
        return self.__envStack.peek()
    

    def stackName(self, symbol: Symbol):
        """
        CSE Rule 1
        
        Pushes the value of the name symbol into the stack.
        """

        self.logger.debug("rule 1")

        if symbol.isType(YStarSymbol):
            self.stack.pushStack(symbol)
            return  
        
        symbol:NameSymbol = symbol
        if symbol.isId() or symbol.isFunction():
            try:
                _value = self.currentEnv().lookUpEnv(symbol.name)
            except Exception as e:
                map = pprint.pformat(self.envMap)
                self.logger.info(f"envMap: {map}")
                self.logger.error(f"Name {symbol.name} not found in the environment tree.")
                raise e
            if (isinstance(_value, EtaClosureSymbol) or isinstance(_value, LambdaClosureSymbol) 
                or isinstance(_value, FunctionSymbol)):
                symbol = _value
            else:
                symbol = NameSymbol(_value)

        self.stack.pushStack(symbol)
        
    def stackLambda(self, _lambda: LambdaSymbol):
        """
        CSE Rule 2
        
        Pushes a lambda closure into the stack.
        """

        self.logger.debug("rule 2")
        __currentEnvIndex = self.currentEnv().getIndex()
        self.stack.pushStack(LambdaClosureSymbol(_lambda.variables, _lambda.index, __currentEnvIndex))         
            
    def applyLambda(self, top:LambdaClosureSymbol):
        """
        CSE Rule 4 and CSE Rule 11 and also Rule 12, 13
        
        This function evaluates n-ary functions as well.
        Creates a new environment and make it the current environment.
        Also Insert environment data for env_variables with the respective env_values.
        """	
 
        self.logger.debug("rule 4/11")
        _lambdaClosure = top
        
        # create new environment
        self.envIndexCounter = self.envIndexCounter + 1
        env_index = self.envIndexCounter
        self.__create_env(env_index, _lambdaClosure.getEnvMarkerIndex())
        
        #Add environment data to the environment            
        env_variables = _lambdaClosure.variables
        
        #Here an error can occur if number of variables != number of values
        num_variables = len(env_variables)
        if num_variables == 1:
            stack_top = self.stack.popStack()
            # if the stack_top is a name symbol, get the value from the environment
            if stack_top.isType(NameSymbol):
                stack_top = stack_top.name
            # else if stack_top is a eta closure, just add it as it is 
            self.currentEnv().insertEnvData(env_variables[0], stack_top)
        else:
            stack_top:NameSymbol = self.stack.popStack()
            tuple_symbol:TupleSymbol = stack_top
            tuple = tuple_symbol.tuple
            for i in range(num_variables):
                # else if stack_top is a eta closure, just add it as it is 
                self.currentEnv().insertEnvData(env_variables[i], tuple[i])

            
        self.__addEnvMarker(env_index)
        self.control.insertControlStruct(self.csMap.get(_lambdaClosure.index))         


    def applyYStar(self):
        """
        CSE Rule 12
        
        This function evaluates the Y* symbol.
        """
        self.logger.debug("rule 12")
        top:LambdaClosureSymbol = self.stack.popStack()
        eta_closure = EtaClosureSymbol.fromLambdaClosure(top)
        self.stack.pushStack(eta_closure)

    def applyFP(self, top: EtaClosureSymbol):
        """
        CSE Rule 13
        
        This function handles the eta closure in the stack.
        """
        self.logger.debug("rule 13")
        lamda_closure = EtaClosureSymbol.toLambdaClosure(top)
        self.stack.pushStack(top)
        self.stack.pushStack(lamda_closure)
        self.control.addGamma()
        self.control.addGamma()

    def __addEnvMarker(self, env_index):
            
        """
        Adds an environment marker to the stack and the control.
        
        """
        self.stack.pushStack(EnvMarkerSymbol(env_index))
        self.control.insertEnvMarker(env_index)
            
    def exitEnv(self, env_marker):
        """
        CSE Rule 5
        
        Exits from the current environment.
        """
        self.logger.debug("rule 5")

        self.stack.removeEnvironment(env_marker)
        self.__envStack.pop()
        
    __operator_map = {
        
        "+": lambda rator, rand: rator + rand,
        "-": lambda rator, rand: rator - rand,
        "*": lambda rator, rand: rator * rand,
        "/": lambda rator, rand: int(rator / rand),
        "or": lambda rator, rand: rator or rand,
        "and": lambda rator, rand: rator and rand,
        "gr": lambda rator, rand: rator > rand,
        "ge": lambda rator, rand: rator >= rand,
        "ls": lambda rator, rand: rator < rand,
        "le": lambda rator, rand: rator <= rand,
        "eq": lambda rator, rand: rator == rand,
        "neg": lambda rator: -rator,
        "not": lambda rator: not rator
        
    }
          
    def binop(self, operator):
        """
        CSE Rule 6
        
        Evaluates Binary Operators and pushes the computed result into the stack.
        """
        self.logger.debug("rule 6")

        rand_1 = self.stack.popStack().name
        rand_2 = self.stack.popStack().name
        try:
            _value = self.__applyOp(operator, rand_1, rand_2)
        except ZeroDivisionError as e:
            print("Division by zero")
            raise e
        self.stack.pushStack(NameSymbol(_value))
        
    def unop(self, operator):
        """"
        CSE Rule 7
        
        Evaluates Unary Operators and pushes the computed result into the stack.
        """
        self.logger.debug("rule 7")

        rand = self.stack.popStack().name
        _value = self.__applyOp(operator, rand)
        self.stack.pushStack(NameSymbol(_value))
            
    def __applyOp(self, operator, rator, rand = None):
        
        """
        
        Applies the operator to the operands.
        
        """ 
        if rand is None:
            return self.__operator_map[operator](rator)
        else:
            return self.__operator_map[operator](rator, rand)
    
    def conditional(self):
        """
        CSE Rule 8
        
        This evaluates the conditional expression.
        Conditional functions are defined in the control structure in the form of delta_then, delta_else, beta, B.
        """
        self.logger.debug("rule 8")

        true_or_false = self.stack.popStack()
        if true_or_false.name == True:
            self.control.removeRightMost()
            _then: DeltaSymbol = self.control.removeRightMost()
            self.control.insertControlStruct(self.csMap.get(_then.index))
        else:
            _else: DeltaSymbol = self.control.removeRightMost()
            self.control.removeRightMost()
            self.control.insertControlStruct(self.csMap.get(_else.index))
        
    def tupleFormation(self, _tau: TauSymbol):
        """
        CSE Rule 9
        """
        self.logger.debug("rule 9")

        i = 0
        n: int = _tau.n
        tupleList = []
        for i in range (n):
            symbol = self.stack.popStack()
            tupleList.append(symbol.name)
            
        new_n_tuple = TupleSymbol(n, tupleList)
        self.stack.pushStack(new_n_tuple)

    def tupleSelection(self, tuple:TupleSymbol):
        """
        CSE Rule 10
        """
        self.logger.debug("rule 10")
        name_symbol:NameSymbol = self.stack.popStack()
        n = name_symbol.name

        self.logger.debug(f"tuple: {tuple}, access n: {n}")
        self.stack.pushStack(NameSymbol(tuple.tuple[n-1]))

    def applyFunction(self, top: FunctionSymbol):
        """
        CSE Rule 14 - Apply Predefined Function
        """
        self.logger.debug("rule 14 - apply function")

        function:DefinedFunction = top.func
        symbol = self.stack.popStack()
        if symbol.isType(LambdaClosureSymbol):
            # add the function NameSymbol to the control again
            self.control.addSymbol(NameSymbol(function.getName()))
            lambda_closure:LambdaClosureSymbol = symbol
            self.applyLambda(lambda_closure)
            return 
        else:
            if isinstance(symbol, TupleSymbol):
                arg = symbol.tuple
            elif isinstance(symbol, NameSymbol):
                value = symbol.name
                if isinstance(value, TupleSymbol):
                    arg = value.tuple
                else:
                    arg = value
            else:
                # for primitive data types
                arg = symbol.name

        function_result = function.run(arg)

        if function_result is not None:
            self.stack.pushStack(NameSymbol(function_result))



