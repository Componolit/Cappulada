
import ir
import ir_template

class Array(ir.Base):

    def __init__(self, ctype, size, constrained=True):
        super(Array, self).__init__()
        self.ctype = ctype
        self.size = size
        self.ctype.SetParent(self)
        self.name = self.ctype.name
        self.constrained = constrained

    def UsedTypes(self, parent):
        return self.ctype.UsedTypes(parent)

    def AdaSpecification(self, indentation=0, private=False):
        return self.ctype.AdaSpecification(indentation, private) + "_Array (1 .. {})".format(self.size)

