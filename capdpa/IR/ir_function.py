import ir
import ir_type
import ir_identifier

class Function(ir.Base):

    def __init__(self, name, symbol, parameters=None, return_type=None):
        super(Function, self).__init__()
        self.name = name
        self.symbol = symbol
        self.parameters = parameters or []
        self.return_type = return_type or ir_type.Type(ir_identifier.Identifier(["void"]), size = 0, is_primitive = True)

    def __repr__(self):
        return "Function(name={}, symbol={}, parameters={}, return_type={})".format(
                self.name, self.symbol, self.parameters, self.return_type)

    def AdaSpecification(self):

        result = "function " if self.return_type else "procedure "
        result += self.name.PackageBaseName()

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
        result += '   with Import => (CPP, "' + self.symbol + '");\n'

        return result

