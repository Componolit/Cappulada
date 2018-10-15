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
        self.return_type = return_type
        if self.return_type:
            self.return_type.parent = self

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
        # TODO
        pass

class Constructor(Function):

    def __init__(self, symbol, parameters=None):
        self.symbol = symbol
        self.parameters = parameters or []
        super(Constructor, self).__init__("__constructor__", symbol, parameters, None)

    def __repr__(self):
        return "Constructor(symbol={}, parameters={})".format(
                self.symbol, self.parameters)

    def AdaSpecification(self, indentation=0):
        return "{0}function Constructor{1} return Class;\n{0}pragma Cpp_Constructor (Constructor, \"{2}\");\n".format(
                " " * indentation,
                " ({})".format("; ".join(
                    map(lambda p: p.AdaSpecification(), self.parameters))) if self.parameters else "", self.symbol)
