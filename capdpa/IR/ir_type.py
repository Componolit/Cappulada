import ir
import ir_template
import mangle

class Type_Reference(ir.Base):

    def __init__(self, name, pointer = 0, constant = False, reference = False, **kwargs):
        super(Type_Reference, self).__init__()
        self.name = name
        self.pointer = pointer
        self.reference = reference
        self.constant = constant

    def AdaSpecification(self, indentation=0, private=""):
        if private:
            name = self.ConvertName(private + "_Private_" + self.name.PackageBaseNameRaw())
        elif self.pointer > 0:
            if self.pointer == 1:
                name = self.name.PackageFullName() + "_Address"
            else:
                raise ValueError("Pointer nesting to deep: {}".format(self.pointer))
        else:
            name = self.name.PackageFullName()
        return " " * indentation + ("access " if self.reference else "") + name

    def FullyQualifiedName(self):
        return self.name.name

    def Mangle(self, package, namedb):
        name = self.FullyQualifiedName()

        result = "P" if self.pointer > 0 else ""
        result += "R" if self.reference else ""
        result += "K" if self.constant else ""

        if name == [package, 'int']:
            result += "i"
        elif name == [package, 'char']:
            result += "c"
        elif name == [package, 'signed_char']:
            result += "c"
        else:
            result += namedb.Get (name[:-1], name[-1])

        return result

class Type_Reference_Template(Type_Reference, ir_template.Template_Reference):

    def __init__(self, name, arguments, pointer = 0, constant = False, reference = False):
        super(Type_Reference_Template, self).__init__(name=name,
              pointer = pointer,
              constant = constant,
              reference = reference)
        self.arguments = arguments

    def AdaSpecification(self, indentation=0, private=""):
        post = "_" + self.ConvertName(self.postfix()[1:])
        return super(Type_Reference_Template, self).AdaSpecification(indentation) + post

    def Mangle(self, package, namedb):
        result = ""

        result += namedb.Get (self.FullyQualifiedName(), None)

        # Template parameter
        result += "I";
        for a in self.arguments:
            result += a.Mangle(package, namedb)

        # FIXME: Not sure whether this delimiter belongs here
        result += "E"

        return result

class Type_Definition(ir.Base):

    def __init__(self, name, reference):
        super(Type_Definition, self).__init__()
        self.name = name
        self.reference = reference

    def AdaSpecification(self, indentation=0):
        return "{0}subtype {1} is {2};".format(
                " " * indentation,
                self.ConvertName(self.name),
                self.reference.AdaSpecification())

    def InstantiateTemplates(self):
        pass
