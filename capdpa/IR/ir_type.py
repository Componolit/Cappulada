import ir;

class Type(ir.Base):

    def __init__(self, name, size, is_primitive=True):
        super(Type, self).__init__()
        self.name = name
        self.size = size
        self.is_primitive = is_primitive

    def __repr__(self):
        return "Type(name={}, size={}, is_primitive={})".format(
                self.name, self.size, self.is_primitive)

    def AdaSpecification(self):
        return self.name.PackageFullName()

