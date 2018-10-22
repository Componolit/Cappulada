import ir
import ir_type

class Variable(ir.Base):

    def __init__(self, name, ctype, access="public"):
        super(Variable, self).__init__()
        self.name = name
        self.ctype = ctype
        self.ctype.SetParent(self)
        self.access = access

    def AdaSpecification(self, indentation=0):
        return " " * indentation + "%(private)s%(name)s : %(type)s" % \
                { 'private' : "" if self.access == "public" else "Private_",
                  'name': self.ConvertName(self.name),
                  'type': self.ctype.AdaSpecification(access=self.access) }

    def InstantiateTemplates(self):
        if isinstance(self.ctype, ir_type.Type_Reference_Template):
            template = self.GetRoot()[self.ctype.FullyQualifiedName()[1:]]
            instance = template.instantiate(self.ctype)
            if instance not in template.parent.children:
                index = template.parent.children.index(template) + template.parent_index
                template.parent.children.insert(index, instance)
                #FIXME: set instance parent correctly
                template.parent_index += 1
