import ir

class Constant(ir.Base):

    def __init__(self, name, value):
        super(Constant, self).__init__()
        self.name = name
        self.value = value

    def __repr__(self):
        return "Constant(name={}, value={})".format(
                self.name, self.value)

    def AdaSpecification(self, indentation=0):
        return " " * indentation + self.ConvertName(self.name) + " : constant := " + str(self.value) + ";"
