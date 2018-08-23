import cxx

class Constant(cxx.Base):

    def __init__(self, name, value=None):
        super(Constant, self).__init__()
        self.name = name
        self.value = value

    def AdaSpecification(self):
        return self.name.PackageBaseName() + " : constant := " + str(self.value) + ";"
