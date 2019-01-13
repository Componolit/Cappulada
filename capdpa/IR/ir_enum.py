import ir

class Enum(ir.Base):

    def __init__(self, name, children=None, ctype=None):
        super(Enum, self).__init__()
        self.name       = name
        self.children  = children or []
        self.ctype = ctype
        self._parentize_list(self.children)

    def AdaSpecification(self, indentation=0):
        return "{indent}type {name} is ({elements}){size};\n{indent}for {name} use ({representation});".format(
                indent         = " " * indentation,
                name           = self.ConvertName(self.name),
                size           = "\n{indent}with Size => {ctype}'Size".format(
                                    ctype  = self.ctype.AdaSpecification(),
                                    indent = " " * indentation) if self.ctype else "",
                elements       = ", ".join(map(lambda c: self.ConvertName(c.name), self.children)),
                representation = ", ".join(map(lambda c: self.ConvertName(c.name) + " => " + str(c.value), self.children)))
