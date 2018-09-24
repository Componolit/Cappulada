import ir
import ir_class
import ir_constant
import ir_enum
import ir_type

class Namespace(ir.Base):

    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []
        self._parentize_list(self.children)
        super(Namespace, self).__init__()

    def __repr__(self):
        return "Namespace(name={}, children={})".format(self.name, self.children)

    def AdaSpecification(self, indentation=0):
        fqn_ada = ".".join(map(lambda name: self.ConvertName(name), self.FullyQualifiedName()))

        compilation_units = [
                "package {0}\nis{1}\nend {0};\n"
                .format(
                    fqn_ada,
                    "\n".join([""] + map(
                        lambda c: c.AdaSpecification(indentation=3),
                        filter(
                            lambda c: ir_constant.Constant.isInst(c) or ir_enum.Enum.isInst(c) or ir_type.Type_Definition.isInst(c),
                            self.children)))
                )]
        for p in self.children:
            if isinstance(p, Namespace):
                compilation_units.extend(p.AdaSpecification())
            if isinstance(p, ir_class.Class):
                compilation_units.append(p.AdaSpecification())

        return compilation_units
