import cxx;

class Variable(cxx.Base):

    def __init__(self, name, ctype):
        super(Variable, self).__init__()
        self.name = name
        self.ctype = ctype

    def AdaSpecification(self):
        return "%(name)s : %(type)s;" % \
               { 'name': self.ConvertIdentifier(self.name),
                 'type': self.ConvertType(self.ctype) }
