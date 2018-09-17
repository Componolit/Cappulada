import ir
import ir_constant
import ir_enum
import ir_function
import ir_identifier
import ir_variable

class NotImplemented(Exception):

    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Class(ir.Base):

    def __init__(self, name, children=None):

        super(Class, self).__init__()
        self.name       = name
        self.children   = children or []
        self._parentize_list(self.children)

    def __repr__(self):
        return "Class(name={}, children={})".format(self.name, self.children)

    def UsedPackages(self):
        types = []
        isFunction = lambda f: isinstance(f, ir_function.Function)
        isVariable = lambda v: isinstance(v, ir_variable.Variable)
        isLocalType = lambda t: t.name.PackagePath() and t.name.PackagePath() != self.FullyQualifiedName()

        for f in filter(isFunction, self.children):
            map(lambda p: types.append(p.ctype), f.parameters)
            if f.return_type:
                types.append(f.return_type)

        map(lambda v: types.append(v.ctype), filter(isVariable, self.children))

        return sorted(list(set(map(lambda t: t.name.PackagePathName(), filter(isLocalType, types)))))

    def AdaSpecification(self):

        # Generate with statements
        withs = ""
        for w in self.UsedPackages():
            withs += "with " + w + ";\n"
        if withs:
            withs += "\n"

        # Generate record members
        null = type("", (), dict(AdaSpecification=lambda self: "null"))()
        isVar = lambda e: isinstance(e, ir_variable.Variable)

        class_record = '   type %(type)s is\n   tagged limited '
        class_record += "record\n"
        for member in filter(isVar, self.children) or [null]:
            class_record += "      " + member.AdaSpecification() + ";\n"
        class_record += "   end record\n"
        class_record += "   with Import => CPP;\n"
        class_record = class_record  % { 'type': self.ConvertName(self.name) }

        # Generate functions and procedures
        isOp = lambda e: isinstance(e, ir_function.Function) or isinstance(e, ir_function.Constructor)
        ops = filter(isOp, self.children)

        # Generate constants
        isConst = lambda e: isinstance(e, ir_constant.Constant) or isinstance(e, ir_enum.Enum)
        constants = filter(isConst, self.children)

        # Main package structure
        p = \
            '%(withs)s'                                 + \
            'package %(package)s\n'                     + \
            'is\n'                                      + \
            '%(constants)s'                             + \
            '%(record)s'                                + \
            '%(ops)s'                                   + \
            'end %(package)s;\n'

        specOf = lambda obj: "   " + obj.AdaSpecification() + (
                (";\n   " + obj.AdaRepresentation() + ";") if isinstance(obj, ir_enum.Enum) and obj.has_values else ";")

        return p % { 'withs':       withs,
                     'package':     ".".join([self.ConvertName(name) for name in self.FullyQualifiedName()]),
                     'constants':   "\n".join(map(specOf, constants) + [""]),
                     'record':      class_record,
                     'ops':         "".join(["   " + o.AdaSpecification() for o in ops]) }
