import ir

class Constant(ir.Base):

    def __init__(self, name, value, ctype=None):
        super(Constant, self).__init__()
        self.name = name
        self.value = value
        self.ctype = ctype

    def AdaSpecification(self, indentation=0):
        return "{indent}{name} : constant {ctype}:= {value};".format(
            indent = " " * indentation,
            name   = self.ConvertName(self.name),
            ctype  = self.ctype.AdaSpecification() + " " if self.ctype else "",
            value  = str(self.value))

    def UsedTypes(self, parent):
        if self.ctype:
            return [self.ctype.UsedTypes(parent)]
        return []

    def InstantiateTemplates(self):
        pass
