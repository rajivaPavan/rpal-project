from rpal_interpreter.cse_control_structures import CSInitializer
from rpal_interpreter.trees import STNode
from .symbol import *
from .cse_components import *
import logger

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
        self.env = Environment(index,parent)
        self.envMap[index] = self.env
        

    def evaluate(self):
        
        """Evaluates the Control."""
        
        self.logger.debug(f"control {self.control}")
        self.logger.debug(f"stack {self.stack}")

        right_most = self.control.removeRightMost()

        if right_most is None:
            final_result = self.stack.popStack().name
            return final_result

        elif right_most.isType(NameSymbol) or right_most.isType(YStarSymbol):
            self.stackName(right_most)       
              
        elif right_most.isType(LambdaSymbol):
            _lambda = right_most
            self.stackLambda(_lambda)
            
        elif right_most.isType(GammaSymbol):
            self.applyLambda()
                   
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
        if symbol.checkNameSymbolType(str):
            _value = self.env.lookUpEnv(symbol.name)
            if isinstance(_value, EtaClosureSymbol):
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
        __currentEnvIndex = self.env.envMarker.envIndex
        self.stack.pushStack(LambdaClosureSymbol(_lambda.variables, _lambda.index, __currentEnvIndex))         
            
    def applyLambda(self):
        """
        CSE Rule 4 and CSE Rule 11
        
        This function evaluates n-ary functions as well.
        Creates a new environment and make it the current environment.
        Also Insert environment data for env_variables with the respective env_values.
        """	

        top = self.stack.popStack() 
        
        if top.isType(YStarSymbol):
            # Rule 12
            self.applyYStar()
        elif top.isType(EtaClosureSymbol):
            # Rule 13
            self.applyFP(top)
        
        elif top.isType(LambdaClosureSymbol):
            
            self.logger.debug("rule 4/11")

            _lambdaClosure: LambdaClosureSymbol = top
            
            # create new environment
            self.envIndexCounter = self.envIndexCounter + 1
            env_index = self.envIndexCounter
            self.__create_env(env_index, _lambdaClosure.getEnvMarkerIndex())
            
            #Add environment data to the environment            
            env_variables = _lambdaClosure.variables
            
            #Here an error can occur if number of variables != number of values
            for i in range(len(env_variables)):
                stack_top = self.stack.popStack()
                # if the stack_top is a name symbol, get the value from the environment
                if stack_top.isType(NameSymbol):
                    stack_top = stack_top.name
                # else if stack_top is a eta closure, just add it as it is 
                self.env.insertEnvData(env_variables[i], stack_top)
                
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
        self.logger.debug(f"add env marker {env_index}")
        self.stack.pushStack(EnvMarkerSymbol(env_index))
        self.control.insertEnvMarker(env_index)
            
    def exitEnv(self, env_marker):
        """
        CSE Rule 5
        
        Exits from the current environment.
        """
        
        self.stack.removeEnvironment(env_marker)
        self.env = self.env.parent
        
    __operator_map = {
        
        "+": lambda rator, rand: rator + rand,
        "-": lambda rator, rand: rator - rand,
        "*": lambda rator, rand: rator * rand,
        "/": lambda rator, rand: rator / rand,
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
        rand_1 = self.stack.popStack().name
        rand_2 = self.stack.popStack().name

        _value = self.__applyOp(operator, rand_1, rand_2)
        self.stack.pushStack(NameSymbol(_value))
        
    def unop(self, operator):
        """"
        CSE Rule 7
        
        Evaluates Unary Operators and pushes the computed result into the stack.
        """
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
        i = 0
        n: int = _tau.n
        tupleList = []
        for i in range (n):
            tupleList.append(self.stack.popStack())
            
        new_n_tuple = TauSymbol(n, tupleList)
        self.stack.pushStack(new_n_tuple)
