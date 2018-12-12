import ir
import ir_identifier
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
        return namedb.Get (name[:-1], name[-1], self.pointer, self.constant, self.reference)

class Type_Literal(Type_Reference):
    """
    Not really a type but a literal value that is used to instantiate a template
    """

    def __init__(self, value, **kwargs):
        super(Type_Literal, self).__init__(name=ir_identifier.Identifier([str(value)]))
        self.value = value

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

        result += namedb.Get (self.FullyQualifiedName(), None, self.pointer, self.constant, self.reference)

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
        if self.reference:
            return "{0}subtype {1} is {2};".format(
                    " " * indentation,
                    self.ConvertName(self.name),
                    self.reference.AdaSpecification())
        else:
            return ("{0}package {1} is\n"
                    "{0}{0}type Class is null record;\n"
                    "{0}{0}type Class_Address is new System.Address;\n"
                    "{0}end {1};").format(
                            " " * indentation,
                            self.ConvertName(self.name))

    def isVirtual(self):
        return False

    def Members(self):
        return []

    def InstantiateTemplates(self):
        pass
