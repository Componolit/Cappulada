import ir
import ir_type
import ir_identifier

class Function(ir.Base):

    def __init__(self, name, symbol, parameters=None, return_type=None):
        super(Function, self).__init__()
        self.name = name
        self.symbol = symbol
        self.parameters = parameters or []
        self._parentize_list(self.parameters)
        self.return_type = return_type or ir_type.Type_Reference(ir_identifier.Identifier(["void"]))

    def __repr__(self):
        return "Function(name={}, symbol={}, parameters={}, return_type={})".format(
                self.name, self.symbol, self.parameters, self.return_type)

    def AdaSpecification(self):

        result = "function " if self.return_type else "procedure "
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

        result += " return " + self.return_type.AdaSpecification() + "\n"
        result += '   with Import, Convention => CPP, External_Name => "' + self.symbol + '";\n'

        return result

class Constructor(Function):

    def __init__(self, symbol, parameters=None):
        self.symbol = symbol
        self.parameters = parameters or []
        super(Constructor, self).__init__("__constructor__", symbol, parameters, None)

    def __repr__(self):
        return "Constructor(symbol={}, parameters={})".format(
                self.symbol, self.parameters)

    def AdaSpecification(self):
        return "function Constructor{} return {};\n   pragma Cpp_Constructor (Constructor, \"{}\");\n".format(
                " ({})".format("; ".join([p.AdaSpecification() for p in self.parameters])) if self.parameters else "",
                           self.ConvertName(self.parent.name), self.symbol)
