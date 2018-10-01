import ir;

class Type_Reference(ir.Base):

    def __init__(self, name, pointer = 0):
        super(Type_Reference, self).__init__()
        self.name = name
        self.pointer = pointer

    def __repr__(self):
        return "Type_Reference(name={}, pointer={})".format(
                self.name,
                self.pointer)

    def AdaSpecification(self, indentation=0):
        return " " * indentation + ("access " if self.pointer else "") + self.name.PackageFullName()


class Type_Definition(ir.Base):

    def __init__(self, name, reference):
        super(Type_Definition, self).__init__()
        self.name = name
        self.reference = reference

    def __repr__(self):
        return "Type_Definition(name={}, reference={})".format(
                self.name, self.reference)

    def AdaSpecification(self, indentation=0):
        return "{0}subtype {1} is {2};".format(
                " " * indentation,
                self.ConvertName(self.name),
                self.reference.AdaSpecification())
