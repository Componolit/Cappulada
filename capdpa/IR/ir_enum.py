import ir

class Enum(ir.Base):

    def __init__(self, name, children=None):
        super(Enum, self).__init__()
        self.name       = name
        self.children  = children or []
        self._parentize_list(self.children)
        self.has_values = False

        for c in self.children:
            if c.value:
                self.has_values = True

    def __repr__(self):
        return "Enum(name={}, children={})".format(
                self.name, self.children)

    def HasValues(self):
        return self.has_values

    def AdaSpecification(self):
        result = "type " + self.ConvertName(self.name) + " is ("
        first = True
        for c in self.children:
            if not first:
                result += ", "
            first = False
            result += self.ConvertName(c.name)
        result += ")"
        return result

    def AdaRepresentation(self):
        result = "for " + self.ConvertName(self.name) + " use ("
        first = True
        for c in self.children:
            if not first:
                result += ", "
            first = False
            result += self.ConvertName(c.name) + " => " + str(c.value)
        result += ")"
        return result
