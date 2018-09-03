import ir;

class Variable(ir.Base):

    def __init__(self, name, ctype):
        super(Variable, self).__init__()
        self.name = name
        self.ctype = ctype

    def __repr__(self):
        return "Variable(name={}, ctype={})".format(
                self.name, self.ctype)

    def AdaSpecification(self):
        return "%(name)s : %(type)s" % \
               { 'name': self.ConvertName(self.name),
                 'type': self.ctype.AdaSpecification() }

