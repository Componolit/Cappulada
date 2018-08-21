import cxx

class Enum(cxx.Base):

    def __init__(self, name, constants=None):
        super(Enum, self).__init__()
        self.name = name
        self.constants = constants or []
