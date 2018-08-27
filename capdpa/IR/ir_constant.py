import ir

class Constant(ir.Base):

    def __init__(self, name, value=None):
        super(Constant, self).__init__()
        self.name = name
        self.value = value

    def __repr__(self):
        return "Constant(name={}, value={})".format(
                self.name, self.value)

    def AdaSpecification(self):
        return self.name.PackageBaseName() + " : constant := " + str(self.value) + ";"
