
import ir
import ir_template

class Array(ir.Base):

    def __init__(self, ctype, size):
        super(Array, self).__init__()
        self.ctype = ctype
        self.size = size
        self.ctype.SetParent(self)

    def UsedTypes(self, parent):
        return self.ctype.UsedTypes(parent)

class Array_Template(Array, ir_template.Template_Reference):

    def __init__(self, ctype, argument):
        super(Array_Template, self).__init__(ctype=ctype, size=0)
