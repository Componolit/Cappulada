import ir
import ir_class
import ir_constant
import ir_enum

class Namespace(ir.Base):

    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []
        self._parentize_list(self.children)
        super(Namespace, self).__init__()

    def __repr__(self):
        return "Namespace(name={}, children={})".format(self.name, self.children)

    def AdaEnumSpecification(self):
        enums = ""
        for e in self.enums:
            enums += "   " + e.AdaSpecification() + ";\n"
            if e.HasValues():
                enums += "   " + e.AdaRepresentation() + ";\n"
        return enums

    def AdaConstantSpecification(self):
        constants = ""
        for c in self.constants:
            constants += "   " + c.AdaSpecification() + "\n"
        return constants

    def AdaSpecification(self):
        fqn_ada = ".".join([self.ConvertName(name) for name in self.FullyQualifiedName()])
        indent = lambda line: "   " + line
        compilation_units = [
                "package {}\nis{}\nend {};\n"
                .format(
                    fqn_ada,
                    "\n".join([""] + map(indent, [c.AdaSpecification() + ";" for c in self.children if
                        isinstance(c, ir_constant.Constant) or
                        isinstance(c, ir_enum.Enum)])),
                    fqn_ada
                )]
        for p in self.children:
            if isinstance(p, Namespace):
                compilation_units.extend(p.AdaSpecification())
            if isinstance(p, ir_class.Class):
                compilation_units.append(p.AdaSpecification())

        return compilation_units
