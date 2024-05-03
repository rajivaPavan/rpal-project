class CSEmachine:
    
    def __init__(self, st):
        self.control = Control(st)
        self.env = Environment()
        self.stack = Stack()
    

    def evaluate(self):
        right_most = self.control.removeRightMost()
        
    

    
    
class Control:
    
    def __init__(self, st):
        self.controlStructs = st.preorderTraverse()
        self.control = ['e0'].insertControlStructs.self.controlStructs[0]
        
    def preOrderTraverse(self):
        pass
    
    def removeRightMost(self):
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStructs(self, controlStructs):
        for i in controlStructs:
            self.control.append(i)
            
    
    
    
        
class Stack:
    def __init__(self):
        self.__stack = []
    
    def popStack(self):
        self.stack.pop(0)
    
    def pushStack(self, value):
        self.stack.append(value)
        
    def remove(self, value):
        self.remove(value)
        
    def calculate(self):
        pass
    
    
    
class Environment:
    def __init__(self):
        pass
    
        

class GammaNode:
    pass

class LambdaNode:
    pass
    
class OperatorNode:
    pass


    
    