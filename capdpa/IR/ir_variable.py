import ir
import ir_type
import mangle

class NamedType(ir.Base):

    def __init__(self, name, ctype):
        super(NamedType, self).__init__()
        self.name = name
        self.ctype = ctype
        self.ctype.SetParent(self)

    def InstantiateTemplates(self):
        if isinstance(self.ctype, ir_type.Type_Reference_Template):
            template = self.GetRoot()[self.ctype.FullyQualifiedName()[1:]]
            instance = template.instantiate(self.ctype)
            if instance not in template.parent.children:
                index = template.parent.children.index(template) + template.parent_index
                template.parent.children.insert(index, instance)
                #FIXME: set instance parent correctly
                template.parent_index += 1

class Argument(NamedType):

    def __init__(self, name, ctype):
        super(Argument, self).__init__(name, ctype)

    def AdaSpecification(self, indentation=0):
        return " " * indentation + "%(name)s : %(type)s" % \
                { 'name': self.ConvertName(self.name),
                  'type': self.ctype.AdaSpecification() }

    def Mangle(self):
        return self.ctype.Mangle()

class Variable(NamedType):

    def __init__(self, name, ctype):
        super(Variable, self).__init__(name, ctype)

    def AdaSpecification(self, indentation=0):
        return (" " * indentation + "%(name)s : %(type)s\n" + " " * indentation + "%(with)s") % \
                { 'name': self.ConvertName(self.name),
                  'type': self.ctype.AdaSpecification(),
                  'with': 'with Import, Convention => CPP, External_Name => "' + str(self.Mangle()) + '";\n' }

    def Mangle(self):

        fqn = self.parent.FullyQualifiedName()

        if len(fqn) == 1:
            return self.name

        name = mangle.Name ([mangle.String(n) for n in fqn[1:]], mangle.String(self.name))
        return mangle.Symbol ([mangle.Nested(name)])

class Member(NamedType):

    def __init__(self, name, ctype, access="public", constant=False):
        super(Member, self).__init__(name, ctype)
        self.access = access
        self.constant = constant

    def AdaSpecification(self, indentation=0, private_name=""):
        return " " * indentation + "%(constant)s%(private)s%(name)s : aliased %(type)s" % \
                { 'constant': "" if not self.constant or self.access != "public" else "Constant_",
                  'private' : "" if self.access == "public" else "Private_",
                  'name': self.ConvertName(self.name),
                  'type': self.ctype.AdaSpecification(private=("" if self.access == "public" else private_name)) }

    def IsPrivate(self):
        return self.access != "public"
