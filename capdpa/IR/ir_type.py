import ir;

class Type_Reference(ir.Base):

    def __init__(self, name, pointer = 0, builtin = True):
        super(Type_Reference, self).__init__()
        self.name = name
        self.pointer = pointer
        self.builtin = builtin

    def __repr__(self):
        return "Type_Reference(name={}, pointer={}, builtin={})".format(
                self.name,
                self.pointer,
                self.builtin)

    def AdaSpecification(self):
        return self.name.PackageFullName()


class Type_Definition(ir.Base):

    def __init__(self, name, reference):
        super(Type_Definition, self).__init__()
        self.name = name
        self.reference = reference

    def __repr__(self):
        return "Type_Definition(name={}, reference={})".format(
                self.name, self.reference)
