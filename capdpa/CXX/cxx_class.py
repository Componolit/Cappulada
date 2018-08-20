
class Class:

    def __init__(self, name, constructor=None, members=None, functions=None):
        self.name = name
        self.constructor = constructor
        self.members = members or []
        self.functions = functions or []
