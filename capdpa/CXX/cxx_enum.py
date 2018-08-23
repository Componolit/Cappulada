import cxx

class Enum(cxx.Base):

    def __init__(self, name, constants=None):
        super(Enum, self).__init__()
        self.name = name
        self.constants = constants or []

        for c in self.constants:
            if c.value:
                raise Exception("Element " + c.name.PackageBaseName() +
                                " of enum " + self.name.PackageBaseName() +
                                " must not have a value");

    def AdaSpecification(self):
        result = "type " + self.name.PackageBaseName() + " is ("
        first = True
        for c in self.constants:
            if not first:
                result += ", "
            first = False
            result += c.name.PackageBaseName()
        result += ")"
        return result
