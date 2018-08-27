import ir;

class Variable(ir.Base):

    def __init__(self, name, ctype):
        super(Variable, self).__init__()
        self.name = name
        self.ctype = ctype

    def AdaSpecification(self):
        return "%(name)s : %(type)s" % \
               { 'name': self.name.PackageFullName(),
                 'type': self.ctype.AdaSpecification() }
