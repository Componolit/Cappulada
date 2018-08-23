import cxx

class Function(cxx.Base):

    def __init__(self, name, symbol, parameters=None, return_type=None):
        super(Function, self).__init__()
        self.name = name
        self.symbol = symbol
        self.parameters = parameters or []
        self.return_type = return_type # or void

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
        result += '   with Symbol => "' + self.symbol + '";\n'

        return result
