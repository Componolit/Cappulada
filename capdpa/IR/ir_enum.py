import ir

class Enum(ir.Base):

    def __init__(self, name, children=None):
        super(Enum, self).__init__()
        self.name       = name
        self.children  = children or []
        self._parentize_list(self.children)

    def AdaSpecification(self, indentation=0):
        return "{0}type {1} is ({2});\n{0}for {1} use ({3});".format(
                " " * indentation,
                self.ConvertName(self.name),
                ", ".join(map(lambda c: self.ConvertName(c.name), self.children)),
                ", ".join(map(lambda c: self.ConvertName(c.name) + " => " + str(c.value), self.children)))
