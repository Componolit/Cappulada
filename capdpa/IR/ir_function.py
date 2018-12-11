import ir
import ir_type
import ir_identifier
import mangle

class Function(ir.Base):

    def __init__(self, name, symbol, parameters=None, return_type=None, virtual=False):
        super(Function, self).__init__()
        self.name = name
        self.symbol = symbol
        self.parameters = parameters or []
        self._parentize_list(self.parameters)
        self.return_type = return_type
        if self.return_type:
            self.return_type.parent = self
        self.virtual = virtual

    def isVirtual(self):
        return self.virtual

    def AdaSpecification(self, indentation=0):

        result = " " * indentation + ("function " if self.return_type else "procedure ")
        result += self.ConvertName(self.name)

        if self.parameters:
            result += " ("
            first = True
            for p in self.parameters:
                if not first:
                    result += "; "
                first = False
                result += p.AdaSpecification()
            result += ")"

        result += (" return " + self.return_type.AdaSpecification() + "\n") if self.return_type else "\n"
        result += " " * indentation + 'with Import, Convention => CPP, External_Name => "' + self.symbol + '";\n'

        return result

    def InstantiateTemplates(self):
        pass

    def Mangle(self, package):

        namedb = mangle.Namedb()

        # Mangled-name prefix "_Z"
        result = "_Z"

        if not self.parent:
            raise Exception ("Parent not set")

        result += namedb.Get (self.parent.FullyQualifiedName(), self.name)

        # parameters
        if self.parameters:
            for p in self.parameters:
                result += p.Mangle(package, namedb)
        else:
            result += "v"

        return result

class Function_Reference(Function):

    def __init__(self, parameters=None, return_type=None, pointer=1, reference=False):
        super(Function_Reference, self).__init__(name="", symbol="", parameters=parameters, return_type=return_type, virtual=False)
        self.name = ir_identifier.Identifier([])
        self.pointer = pointer
        self.reference = reference

        if self.pointer == 0 and not self.reference:
            raise Exception ("Invalid function reference (neither ref nor pointer)")

    def AdaSpecification(self, indentation=0, private=""):
        if private == "":
            args = " ({})".format("; ".join(a.AdaSpecification() for a in self.parameters)) if self.parameters else ""
            kind = "function" if self.return_type else "procedure"
            ret = " return {}".format(self.return_type.AdaSpecification()) if self.return_type else ""
            name = "access " + kind + args + ret
        else:
            name = "Private_Procedure"
        return " " * indentation + name

    def Mangle(self, package, namedb):

        result = ""

        if self.reference:
            result += "R"
        else:
            result += "P"

        result += "F"

        # return type
        result += self.return_type.Mangle(package, namedb)

        # parameters
        if self.parameters:
            for p in self.parameters:
                result += p.Mangle(package, namedb)
        else:
            result += "v"

        result += "E"

        return result

class Constructor(Function):

    def __init__(self, symbol, parameters=None):
        super(Constructor, self).__init__("__constructor__", symbol, parameters, None)
        self.symbol = symbol
        self.parameters = parameters or []

    def __repr__(self):
        return "Constructor(symbol={}, parameters={})".format(
                self.symbol, self.parameters)

    def AdaSpecification(self, indentation=0):
        return "{0}function Constructor{1} return Class;\n{0}pragma Cpp_Constructor (Constructor, \"{2}\");\n".format(
                " " * indentation,
                " ({})".format("; ".join(
                    map(lambda p: p.AdaSpecification(), self.parameters))) if self.parameters else "", self.symbol)
