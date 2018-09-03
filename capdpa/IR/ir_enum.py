import ir

class Enum(ir.Base):

    def __init__(self, name, constants=None):
        super(Enum, self).__init__()
        self.name       = name
        self.constants  = constants or []
        self._parentize_list(self.constants)
        self.has_values = False

        for c in self.constants:
            if c.value:
                self.has_values = True

    def __repr__(self):
        return "Enum(name={}, constants={})".format(
                self.name, self.constants)

    def HasValues(self):
        return self.has_values

    def AdaSpecification(self):
        result = "type " + self.ConvertName(self.name) + " is ("
        first = True
        for c in self.constants:
            if not first:
                result += ", "
            first = False
            result += self.ConvertName(c.name)
        result += ")"
        return result

    def AdaRepresentation(self):
        result = "for " + self.ConvertName(self.name) + " use ("
        first = True
        for c in self.constants:
            if not first:
                result += ", "
            first = False
            result += self.ConvertName(c.name) + " => " + str(c.value)
        result += ")"
        return result
