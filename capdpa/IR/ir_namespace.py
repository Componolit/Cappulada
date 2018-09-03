import ir

class Namespace(ir.Base):

    def __init__(self, name, namespaces=None, classes=None, constants=None, enums=None):
        self.name = name
        self.namespaces = namespaces or []
        self.classes = classes or []
        self.constants = constants or []
        self.enums = enums or []
        self._parentize_list(self.namespaces)
        self._parentize_list(self.classes)
        self._parentize_list(self.constants)
        self._parentize_list(self.enums)
        super(Namespace, self).__init__()

    def __repr__(self):
        return "Namespace(name={}, namespaces={}, classes={}, constants={}, enums={})".format(
                self.name, self.namespaces, self.classes, self.constants, self.enums)

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
