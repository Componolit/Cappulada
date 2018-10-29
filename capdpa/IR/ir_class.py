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

    def __init__(self, name, children=None):

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

    def isVirtual(self):
        return True in [c.isVirtual() for c in self.children]

    def UsedPackages(self):
        types = []
        isLocalType = lambda t: t.name.PackagePath() and self.FullyQualifiedName()[:len(t.name.PackagePath())] != t.name.PackagePath()

        for f in filter(ir_function.Function.isInst, self.children):
            map(lambda p: types.append(p.ctype), f.parameters)
            if f.return_type:
                types.append(f.return_type)

        map(lambda v: types.append(v.ctype), filter(ir_variable.Variable.isInst, self.children))
        map(lambda t: types.append(t.reference), filter(ir_type.Type_Definition.isInst, self.children))
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

    def AdaSpecification(self, indentation=0):

        # Generate with statements
        withs = ""
        for w in self.UsedPackages():
            withs += "with " + w + ";\n"
        if withs:
            withs += "\n"

        # Generate record members
        null = type("", (), dict(AdaSpecification=lambda self, indentation: " " * indentation + "null"))()
        base = [Class_Reference.isInst(c) for c in self.children]
        base = self.children[base.index(True)] if True in base else None
        hasvirtualbase = base.isVirtual() if base else False

        class_record = '   type Class is{}\n'.format(
                (" new " + base.name.PackageFullName() + " with") if hasvirtualbase and self.isVirtual() else "")
        class_record += '   {}limited '.format("tagged " if self.isVirtual() and not hasvirtualbase else "")
        class_record += "record\n"
        for member in self.Members() or [null]:
            class_record += member.AdaSpecification(indentation=6) + ";\n"
        class_record += "   end record\n"
        class_record += "   with Import, Convention => CPP;\n"
        class_record += "   type Private_Class is limited null record\n"
        class_record += "   with Size => Class'Size;\n"

        # Generate functions and procedures
        isOp = lambda e: ir_function.Function.isInst(e) or ir_function.Constructor.isInst(e)
        ops = filter(isOp, self.children)

        # Generate constants
        isConst = lambda e: ir_constant.Constant.isInst(e) or ir_enum.Enum.isInst(e)
        constants = filter(isConst, self.children)

        # Generate typedefs
        types = filter(ir_type.Type_Definition.isInst, self.children)

        # Main package structure
        p = \
            '%(withs)s'                                 + \
            'package %(package)s\n'                     + \
            'is\n'                                      + \
            '%(types)s'                                 + \
            '%(constants)s'                             + \
            '%(record)s'                                + \
            '%(ops)s'                                   + \
            'end %(package)s;\n'

        return p % { 'withs':       withs,
                     'package':     ".".join(map(self.ConvertName, self.FullyQualifiedName())),
                     'types' :      "\n".join(map(lambda t: t.AdaSpecification(indentation=3), types) + [""]),
                     'constants':   "\n".join(map(lambda c: c.AdaSpecification(indentation=3), constants) + [""]),
                     'record':      class_record,
                     'ops':         "".join(map(lambda o: o.AdaSpecification(indentation=3), ops)) }


class Class_Reference(ir.Base):

    def __init__(self, name):
        self.name = name

    def getClass(self):
        return self.GetRoot()[self.name.PackageFull()[1:]]

    def isVirtual(self):
        return self.getClass().isVirtual()

    def InstantiateTemplates(self):
        pass
