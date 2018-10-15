import ir
import ir_type

class Variable(ir.Base):

    def __init__(self, name, ctype):
        super(Variable, self).__init__()
        self.name = name
        self.ctype = ctype
        self.ctype.SetParent(self)

    def __repr__(self):
        return "Variable(name={}, ctype={})".format(
                self.name, self.ctype)

    def AdaSpecification(self, indentation=0):
        return " " * indentation + "%(name)s : %(type)s" % \
               { 'name': self.ConvertName(self.name),
                 'type': self.ctype.AdaSpecification() }

    def InstantiateTemplates(self):
        if isinstance(self.ctype, ir_type.Type_Reference_Template):
            template = self.GetRoot()[self.ctype.FullyQualifiedName()[1:]]
            instance = template.instantiate(self.ctype)
            if instance not in template.parent.children:
                index = template.parent.children.index(template) + template.parent_index
                template.parent.children.insert(index, instance)
                template.parent_index += 1
