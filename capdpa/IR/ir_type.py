import ir;

class Type_Reference(ir.Base):

    def __init__(self, name):
        super(Type_Reference, self).__init__()
        self.name = name

    def __repr__(self):
        return "Type(name={})".format(self.name)

    def AdaSpecification(self):
        return self.name.PackageFullName()

