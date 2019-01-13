import ir
import ir_constant
import ir_enum
import ir_function
import ir_identifier
import ir_type
import ir_variable
import ir_unit
from copy import copy

class Class(ir_unit.Unit):

    def __init__(self, name, children=None, instanceof=None):

        super(Class, self).__init__()
        self.name       = name
        self.children   = children or []
        if not filter(ir_function.Constructor.isInst, self.children):
            flist = [ir_function.Function.isInst(c) for c in self.children]
            if True in flist:
                self.children.insert(
                        flist.index(True),
                        ir_function.Constructor(""))
            else:
                self.children.append(ir_function.Constructor(""))
        self._parentize_list(self.children)
        self.instanceof = instanceof

    def isVirtual(self):
        return True in [c.isVirtual() for c in self.children]

    def Members(self):
        members = []
        for c in self.children:
            if ir_unit.Class_Reference.isInst(c) and not c.isVirtual():
                members.append(c)
            if ir_variable.Member.isInst(c):
                members.append(c)
        return members

    def StaticMembers(self, private=False):
        return [v for v in self.children if ir_variable.Variable.isInst(v) and v.IsPrivate() == private]

    def TypeList(self):

        # Generate order-preserving list of unique private types
        types = []
        for t in [copy(m.ctype) for m in self.Members() if m.IsPrivate()]:
            t.reference = False
            t.pointer = 0
            t.const = False
            if t not in types:
                types.append(t)

        return types

    def PublicTypesSpecification(self, indentation):

        types = self.TypeList()
        if not types:
            return ""

        return "\n".join([('{indent}type {private} is limited private;\n{indent}type {private}_Address is limited private;').format(
                            indent = (indentation + 3) * " ",
                            private = t.AdaSpecification(private=True)) for t in types] + ['', ''])

    def PrivatePart(self, indentation):

        result = ("{indent}private\n"
                  "{indent}   pragma SPARK_Mode (Off);\n\n"
                  "{private_static_members}"
                  "{indent}   type Class_Address is access Class;\n").format(
                            indent = (indentation) * " ",
                            private_static_members = "\n".join([m.AdaSpecification(indentation + 3) for m in self.StaticMembers(private=True)]))

        result += "\n".join([('{indent}type {private} is new {basetype};\n{indent}type {private}_Address is access {private};').format(
                            indent = (indentation + 3) * " ",
                            private = t.AdaSpecification(private=True),
                            basetype = t.AdaSpecification()) for t in self.TypeList()])

        return result + "\n";

    def SparkFeatureSet(self):

        return len([c for c in self.children if ir_variable.Member.isInst(c) and ir_function.Function_Reference.isInst(c.ctype)]) == 0

    def AdaSpecification(self, indentation=0):

        # Generate record members
        null = type("", (), dict(AdaSpecification=lambda self, indentation, private_name: " " * indentation + "null"))()
        base = [ir_unit.Class_Reference.isInst(c) for c in self.children]
        base = self.children[base.index(True)] if True in base else None
        hasvirtualbase = base.isVirtual() if base else False

        class_record = (
                "{private_types}"
                "{indent}type Class is{classdef}\n"
                "{indent}{tagged}{limited}record\n"
                "{classmembers}"
                "{indent}end record\n"
                "{indent}with Import, Convention => CPP;\n\n"
                ).format(
                        indent = (indentation + 3) * " ",
                        private_types = self.PublicTypesSpecification(indentation),
                        classdef = (" new " + base.PackageName() + ".Class with") if hasvirtualbase and self.isVirtual() else "",
                        tagged = "tagged " if self.isVirtual() and not hasvirtualbase else "",
                        limited = "limited " if not hasvirtualbase else "",
                        classmembers = "\n".join([m.AdaSpecification(indentation + 6, True) + ";" for m in self.Members() or [null]] + ['']))

        # Generate functions and procedures
        isOp = lambda e: ir_function.Function.isInst(e) or ir_function.Constructor.isInst(e)
        ops = filter(isOp, self.children)

        # Generate constants
        isConst = lambda e: ir_constant.Constant.isInst(e) or ir_enum.Enum.isInst(e)
        constants = filter(isConst, self.children)

        # Generate typedefs
        types = filter(ir_type.Type_Definition.isInst, self.children)

        # Main package structure

        return ("{indent}package {package}\n"
                "{indent}   with SPARK_Mode => {spark_mode}\n"
                "{indent}is\n"
                "{subpackages}"
                "{types}"
                "{constants}"
                "{classrecord}"
                "{static_members}"
                "{indent}   type Class_Address is private;\n\n"
                "{operations}\n"
                "{private}"
                "{indent}end {package};\n").format(
                        indent = indentation * " ",
                        package = self.name if Class.isInst(self.parent) else ".".join(map(self.ConvertName, self.FullyQualifiedName())),
                        spark_mode = "On" if self.SparkFeatureSet() else "Off",
                        subpackages = "\n".join(map(lambda c: c.AdaSpecification(indentation + 3), filter(Class.isInst, self.children))),
                        types = "\n".join(map(lambda t: t.AdaSpecification(indentation + 3), types) + ['']),
                        private = self.PrivatePart(indentation) or "",
                        constants = "\n".join(map(lambda c: c.AdaSpecification(indentation + 3), constants) + ['']),
                        classrecord = class_record,
                        static_members = "\n".join([m.AdaSpecification(indentation + 3) for m in self.StaticMembers()]),
                        operations = "\n".join(map(lambda o: o.AdaSpecification(indentation + 3), ops)))
