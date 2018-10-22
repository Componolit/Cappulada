import ir
import ir_template

class Type_Reference(ir.Base):

    def __init__(self, name, pointer = 0, **kwargs):
        super(Type_Reference, self).__init__()
        self.name = name
        self.pointer = pointer

    def AdaSpecification(self, indentation=0, access="public"):
        if access == "public":
            name = self.name.PackageFullName()
        else:
            name = ".".join(map(
                self.ConvertName,
                self.name.PackageFull()[:1] + [("Private_" + self.name.PackageFull()[-1:][0])]))
        return " " * indentation + ("access " if self.pointer else "") + name

    def FullyQualifiedName(self):
        return self.name.name

class Type_Reference_Template(Type_Reference, ir_template.Template_Reference):

    def __init__(self, name, arguments, pointer = 0):
        super(Type_Reference_Template, self).__init__(name=name, pointer=pointer)
        self.arguments = arguments

    def AdaSpecification(self, indentation=0, access="public"):
        post = "_" + self.ConvertName(self.postfix()[1:])
        return super(Type_Reference_Template, self).AdaSpecification(indentation) + post

class Type_Definition(ir.Base):

    def __init__(self, name, reference):
        super(Type_Definition, self).__init__()
        self.name = name
        self.reference = reference

    def AdaSpecification(self, indentation=0):
        return "{0}subtype {1} is {2};\n{0}type Private_{1} is limited null record\n{0}   with Size => {1}'Size;".format(
                " " * indentation,
                self.ConvertName(self.name),
                self.reference.AdaSpecification())

    def InstantiateTemplates(self):
        pass
