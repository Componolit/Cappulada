import ir
import ir_constant
import ir_enum
import ir_function
import ir_identifier
import ir_type
import ir_variable

class NotImplemented(Exception):

    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Class(ir.Base):

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

    def UsedPackages(self):
        types = [ir_type.Type_Reference(ir_identifier.Identifier(["System", "Address"]))]

        isLocalType = lambda t: t.name.PackagePath() and \
            self.FullyQualifiedName()[:len(t.name.PackagePath())] != t.name.PackagePath() and \
            t.name.PackagePath() not in [c.FullyQualifiedName() for c in self.children]

        for f in filter(ir_function.Function.isInst, self.children):
            map(lambda p: types.append(p.ctype), f.parameters)
            if f.return_type:
                types.append(f.return_type)

        map(lambda v: types.append(v.ctype), filter(ir_variable.Variable.isInst, self.children))
        map(lambda t: types.append(t.reference), filter(lambda c: ir_type.Type_Definition.isInst(c) and c.reference, self.children))
        map(lambda c: types.append(c), filter(Class_Reference.isInst, self.children))

        return sorted(list(set(map(lambda t: t.name.PackagePathName(), filter(isLocalType, types)))))

    def Members(self):
        members = []
        for c in self.children:
            if Class_Reference.isInst(c) and not c.isVirtual():
                members.extend(c.getClass().Members())
            if ir_variable.Variable.isInst(c):
                members.append(c)
        return members

    def PrivateTypesSpecification(self, indentation):

        # Generate order-preserving list of unique private types
        types = []
        for t in [m.ctype for m in self.Members() if m.IsPrivate()]:
            if t not in types:
                types.append(t)

        return "\n".join([('{indent}pragma Warnings (Off, "* bits of ""{private}"" unused");\n' +
                           '{indent}type {private} is null record\n' +
                           '{indent}   with Size => {public}\'Size;\n' +
                           '{indent}pragma Warnings (On, "* bits of ""{private}"" unused");').format(
                            indent = (indentation + 3) * " ",
                            private = t.AdaSpecification(private=self.name),
                            public = t.AdaSpecification()) for t in types] + [''])

    def AdaSpecification(self, indentation=0):

        # Generate record members
        null = type("", (), dict(AdaSpecification=lambda self, indentation, private_name: " " * indentation + "null"))()
        base = [Class_Reference.isInst(c) for c in self.children]
        base = self.children[base.index(True)] if True in base else None
        hasvirtualbase = base.isVirtual() if base else False

        class_record = (
                "{private_types}"
                "{indent}type Class is{classdef}\n"
                "{indent}{tagged}limited record\n"
                "{classmembers}"
                "{indent}end record\n"
                "{indent}with Import, Convention => CPP;\n"
                "{indent}type Class_Address is new System.Address;\n"
                ).format(
                        indent = (indentation + 3) * " ",
                        private_types = self.PrivateTypesSpecification(indentation),
                        classdef = (" new " + base.name.PackageFullName() + " with") if hasvirtualbase and self.isVirtual() else "",
                        tagged = "tagged " if self.isVirtual() and not hasvirtualbase else "",
                        classmembers = "\n".join([m.AdaSpecification(indentation + 6, self.name) + ";" for m in self.Members() or [null]] + ['']))

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
                "{indent}is\n"
                "{subpackages}"
                "{types}"
                "{constants}"
                "{classrecord}"
                "{operations}"
                "{indent}end {package};\n").format(
                        indent = indentation * " ",
                        package = self.name if Class.isInst(self.parent) else ".".join(map(self.ConvertName, self.FullyQualifiedName())),
                        subpackages = "\n".join(map(lambda c: c.AdaSpecification(indentation + 3), filter(Class.isInst, self.children))),
                        types = "\n".join(map(lambda t: t.AdaSpecification(indentation + 3), types) + ['']),
                        constants = "\n".join(map(lambda c: c.AdaSpecification(indentation + 3), constants) + ['']),
                        classrecord = class_record,
                        operations = "".join(map(lambda o: o.AdaSpecification(indentation + 3), ops)))

class Class_Reference(ir.Base):

    def __init__(self, name):
        self.name = name

    def getClass(self):
        return self.GetRoot()[self.name.PackageFull()[1:]]

    def isVirtual(self):
        return self.getClass().isVirtual()

    def InstantiateTemplates(self):
        pass
