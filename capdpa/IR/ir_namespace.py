import ir
import ir_class
import ir_constant
import ir_enum
import ir_type
import ir_variable
import ir_function
import ir_unit

from ..ada import Specification

class Namespace(ir_unit.Unit):

    def __init__(self, name, children=None, with_include="", spec_include="", spec_private=""):
        self.name = name
        self.children = children or []
        self.with_include = with_include
        self.spec_include = spec_include
        self.spec_private = spec_private
        self._parentize_list(self.children)
        super(Namespace, self).__init__()

    def AdaSpecification(self, indentation=0):
        fqn_ada = ".".join(map(lambda name: self.ConvertName(name), self.FullyQualifiedName()))

        if self.UsedPackages():
            withs = "\n".join(map("with {};".format, self.UsedPackages()) + ['', ''])
        else:
            withs = ""

        compilation_units = [
                Specification(
                    name = [self.ConvertName(name) for name in self.FullyQualifiedName()],
                    text = "{withs}{with_include}package {name}\n{spark_mode}is{spec_include}{body}\n{private_include}end {name};\n".format(
                        withs = withs,
                        name  = fqn_ada,
                        body  = "\n".join([""] + map(
                            lambda c: c.AdaSpecification(indentation=3),
                            filter(lambda c: ir_constant.Constant.isInst(c) or
                                             ir_enum.Enum.isInst(c) or
                                             ir_variable.Variable.isInst(c) or
                                             ir_function.Function.isInst(c) or
                                             ir_type.Type_Definition.isInst(c),
                                self.children))),
                        spark_mode = "   with SPARK_Mode => On\n",
                        with_include = self.with_include,
                        spec_include = self.spec_include,
                        private_include = "private\n" + self.spec_private + "\n" if self.spec_private else "",
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
