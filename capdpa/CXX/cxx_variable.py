import cxx;

class Variable(cxx.Base):

    def __init__(self, name, ctype):
        super(Variable, self).__init__()
        self.name = name
        self.ctype = ctype
