import cxx

class Constant(cxx.Base):

    def __init__(self, name, value=0):
        super(Constant, self).__init__()
        self.name = name
        self.value = value

    def AdaSpecification(self):
        return self.name + " : constant := " + str(self.value) + ";"
