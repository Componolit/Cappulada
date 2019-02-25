
import ir
import ir_template
import mangle

class Array(ir.Base):

    def __init__(self, ctype, size):
        super(Array, self).__init__()
        self.ctype = ctype
        self.size = size
        self.ctype.SetParent(self)
        self.name = self.ctype.name

    def UsedTypes(self, parent):
        return self.ctype.UsedTypes(parent)

    def Mangle(self):
        return mangle.Pointer(self.ctype.Mangle())

    def AdaSpecification(self, indentation=0, private=False):
        return self.ctype.AdaSpecification(indentation, private) + "_Array" + (
                " (1 .. {})".format(self.size) if self.size != None else "")

