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

        result = ""

        # C_Address actually means void* which we mangle as a pointer 'P' and
        # a builtin type 'v'. FIXME: Wouldn't it be better to actually set
        # self.pointer and a 'void' type in capdpa/cxx.py?
        result += "P" if self.pointer > 0 or name == [package, "C_Address"] else ""

        result += "K" if self.constant else ""
        result += "R" if self.reference else ""

        # Defined here:
        # https://itanium-cxx-abi.github.io/cxx-abi/abi.html#mangling-builtin
        builtins = {
            'void':                  "v",
            'wchar_t':               'w',
            'bool':                  'b',
            'char':                  'c',
            'signed_char':           'c',  # GCC disagrees with spec (which says 'a')
            'unsigned_char':         'h',
            'short':                 's',
            'unsigned_short':        't',
            'int':                   'i',
            'unsigned_int':          'j',
            'long':                  'l',
            'unsigned_long':         'm',
            'long_long':             'x',
            'unsigned_long_long':    'y',
            '__int128':              'n',
            'unsigned___int128':     'o',
            'float':                 'f',
            'double':                'd',
            'long_double':           'e',
            '__float128':            'g',
            'C_Address':             'v',
        }

        if len(name) == 2 and name[0] == package and name[1] in builtins:
            result += builtins[name[1]]
        else:
            result += namedb.Get (name[:-1], name[-1])

        return result

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
