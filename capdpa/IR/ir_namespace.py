import ir

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
        compilation_units = [
                "package {}\nis\n{}{}end {};\n"
                .format(
                    fqn_ada,
                    self.AdaEnumSpecification(),
                    self.AdaConstantSpecification(),
                    fqn_ada
                )]
        for namespace in self.namespaces:
            compilation_units.extend(namespace.AdaSpecification())
        for c in self.classes:
            compilation_units.append(c.AdaSpecification())

        return compilation_units
