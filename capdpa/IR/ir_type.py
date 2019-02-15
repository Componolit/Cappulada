import ir
import ir_array
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

    def UsedTypes(self, parent):
        fqn = self.FullyQualifiedName()
        if parent == fqn[:-1] or (parent == fqn[:-2] and fqn[-1] == "Class"):
            return []
        return [self.FullyQualifiedName()]

    def AdaSpecification(self, indentation=0, private=False):
        if private:
            name = self.ConvertName("Private_" + self.name.PackageBaseNameRaw())
        elif self.pointer > 0:
            if self.pointer == 1:
                name = self.name.PackageFullName() + "_Address"
            else:
                raise ValueError("Pointer nesting to deep: {}".format(self.pointer))
        else:
            name = self.name.PackageFullName()

        if self.reference and self.FullyQualifiedName()[-1] != "Class":
            name += "_Address"

        return " " * indentation + name

    def FullyQualifiedName(self):
        return self.name.name

    def Mangle(self):

        fqn = self.FullyQualifiedName()

        if fqn[-1] == "Class":
            fqn = fqn[:-1]

        result = mangle.Type ([mangle.String(n) for n in fqn[1:]])

        if self.constant:
            result = mangle.Constant (result)

        if self.reference:
            result = mangle.Reference (result)

        if self.pointer:
            result = mangle.Pointer (result)

        return result

class Type_Literal(Type_Reference):
    """
    Not really a type but a literal value that is used to instantiate a template
    """

    def __init__(self, name, value, **kwargs):
        super(Type_Literal, self).__init__(name)
        self.value = value

    def Mangle(self):
        return mangle.Literal (super(Type_Literal, self).Mangle(), self.value)

class Type_Reference_Template(Type_Reference, ir_template.Template_Reference):

    def __init__(self, name, arguments, pointer = 0, constant = False, reference = False):
        super(Type_Reference_Template, self).__init__(name=name,
              pointer = pointer,
              constant = constant,
              reference = reference)
        self.arguments = arguments

    def PackagePath(self):
        return self.name.name[:-1] + [self.name.name[-1] + self.postfix()]

    def PackageName(self):
        # Add instance postfix
        return ".".join(map(self.ConvertName, self.PackagePath()))

    def AdaSpecification(self, indentation=0, private=False):
        post = "_" + self.ConvertName(self.postfix()[1:])
        return super(Type_Reference_Template, self).AdaSpecification(indentation) + post + ".Class"

    def Mangle(self):

        name = mangle.Name ([mangle.String(n) for n in self.FullyQualifiedName()[1:]])

        # Template parameter
        args = [a.Mangle() for a in self.arguments]

        return mangle.Sequence ([mangle.Nested (name), mangle.Template (args)])

class Type_Definition(ir.Base):

    def __init__(self, name, reference):
        super(Type_Definition, self).__init__()
        self.name = name
        self.reference = reference

    def AdaSpecification(self, indentation=0):
        if self.reference:
            if ir_array.Array.isInst(self.reference):
                return "{0}subtype {1} is {2};".format(
                        " " * indentation,
                        self.ConvertName(self.name),
                        self.reference.AdaSpecification())
            else:
                return "{0}subtype {1} is {2};\n{0}subtype {1}_Array is {2}_Array;".format(
                        " " * indentation,
                        self.ConvertName(self.name),
                        self.reference.AdaSpecification())
        else:
            return ("{0}package {1} is\n"
                    "{0}   type Class is null record;\n"
                    "{0}end {1};").format(
                            " " * indentation,
                            self.ConvertName(self.name))

    def UsedTypes(self, parent):
        return self.reference.UsedTypes(parent) if self.reference else [];

    def isVirtual(self):
        return False

    def Members(self):
        return []

    def InstantiateTemplates(self):
        pass
