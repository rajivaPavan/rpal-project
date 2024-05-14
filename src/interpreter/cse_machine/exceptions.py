
class MachineException(Exception):
    def __init__(self, message):
        super().__init__("An error occured while computing the result.\n" + message)