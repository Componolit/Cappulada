import cxx

class Class(cxx.Base):

    def __init__(self, name, constructor=None, members=None, functions=None):
        super(Class, self).__init__()
        self.name = name
        self.constructor = constructor
        self.members = members or []
        self.functions = functions or []
