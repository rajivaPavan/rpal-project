class ControlElement:
    def __init__(self, type):
        self.type = type
    
class Gamma(ControlElement):
    def __init__(self):
        super().__init__("gamma")
        
class Lambda(ControlElement):
    def __init__(self, variable):
        super().__init__("lambda")
        self.variable = variable
