import ir
import ir_class
import ir_constant
import ir_enum
import ir_type

from ..ada import Specification

class Namespace(ir.Base):

    def __init__(self, name, children=None, with_include="", spec_include=""):
        self.name = name
        self.children = children or []
        self.with_include = with_include
        self.spec_include = spec_include
        self._parentize_list(self.children)
        super(Namespace, self).__init__()

    def AdaSpecification(self, indentation=0):
        fqn_ada = ".".join(map(lambda name: self.ConvertName(name), self.FullyQualifiedName()))

        compilation_units = [
                Specification(
                    name = [self.ConvertName(name) for name in self.FullyQualifiedName()],
                    text = "{with_include}package {name}\nis{spec_include}{body}\nend {name};\n".format(
                        name = fqn_ada,
                        body = "\n".join([""] + map(
                            lambda c: c.AdaSpecification(indentation=3),
                            filter(lambda c: ir_constant.Constant.isInst(c) or ir_enum.Enum.isInst(c) or ir_type.Type_Definition.isInst(c),
                                self.children))),
                        with_include = self.with_include,
                        spec_include = self.spec_include,
                        ))]

        for p in self.children:
            if isinstance(p, Namespace):
                compilation_units.extend(p.AdaSpecification())
            if isinstance(p, ir_class.Class):
                if p.UsedPackages():
                    withs = "\n".join(map("with {};".format, p.UsedPackages()) + ['', ''])
                else:
                    withs = ""
                compilation_units.append(Specification(
                    name = [self.ConvertName(name) for name in p.FullyQualifiedName()],
                    text = withs + p.AdaSpecification()))

        return compilation_units
