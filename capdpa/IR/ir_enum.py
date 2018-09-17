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
        return "type " + self.ConvertName(self.name) + " is ({})".format(
                ", ".join(map(lambda c: self.ConvertName(c.name), self.children)))

    def AdaRepresentation(self):
        return "for " + self.ConvertName(self.name) + " use ({})".format(
                ", ".join(map(lambda c: self.ConvertName(c.name) + " => " + str(c.value), self.children)))
