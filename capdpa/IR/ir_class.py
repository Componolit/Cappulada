import ir
import ir_function
import ir_identifier

class NotImplemented(Exception):

    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Class(ir.Base):

    def __init__(self, name, constructors=None, members=None, functions=None, constants=None, enums=None):

        super(Class, self).__init__()
        self.name         = name
        self.constructors = constructors or [ir_function.Function(name = name, symbol = "")]
        self.members      = members or []
        self.functions    = functions or []
        self.constants    = constants or []
        self.enums        = enums or []
        self._parentize_list(self.constructors)
        self._parentize_list(self.members)
        self._parentize_list(self.functions)
        self._parentize_list(self.constants)
        self._parentize_list(self.enums)

    def __repr__(self):
        return "Class(name={}, constructors={}, members={}, functions={}, constants={}, enums={})".format(
                self.name, self.constructors, self.members, self.functions, self.constants, self.enums)

    def UsedPackages(self):
        types = []
        for f in self.functions:
            for p in f.parameters:
                types.append(p.ctype)
                if f.return_type:
                    types.append(f.return_type)

        for m in self.members:
            types.append(m.ctype)

        used_packages = set()
        for t in types:
            # Local varialbe or fully quallified local type, no package needed
            if not t.name.PackagePath() or t.name.PackagePath() == self.FullyQualifiedName():
                continue
            used_packages.add(t.name.PackagePathName())
        return sorted(list(used_packages))

    def AdaSpecification(self):

        # Generate with statements
        withs = ""
        for w in self.UsedPackages():
            withs += "with " + w + ";\n"
        if withs:
            withs += "\n"

        class_record = ""
        constructors = []
        ops = ""

        if self.constructors:
            # Generate record members
            class_record = '   type %(type)s is\n   tagged limited '
            if self.members:
                class_record += "record\n"
                for member in self.members:
                    class_record += "      " + member.AdaSpecification() + ";\n"
                class_record += "   end record\n"
            else:
                class_record += "null record\n"
            class_record += "   with Import => CPP;\n"
            class_record = class_record  % { 'type': self.ConvertName(self.name) }

            # generate constructors
            constructors = [
                ('   function Constructor%(args)s return %(type)s;\n' + \
                 '   pragma Cpp_Constructor (Constructor, "%(symbol)s");\n') \
                   % { 'type':   self.ConvertName(self.name),
                       'symbol': constructor.symbol,
                       'args' : " (" + "; ".join([
                           self.ConvertName(arg.name) +
                           " : " +
                           arg.ctype.name.PackageBaseName()
                           for arg in constructor.parameters]) + ")"
                       if constructor.parameters else ""} for constructor in self.constructors]

            # generate primitive operations for tagged type
            ops=""
            if self.functions:
                for f in self.functions:
                    ops += "   " + f.AdaSpecification()

        enums = ""
        for e in self.enums:
            enums += "   " + e.AdaSpecification() + ";\n"
            if e.HasValues():
                enums += "   " + e.AdaRepresentation() + ";\n"

        constants = ""
        for c in self.constants:
            constants += "   " + c.AdaSpecification() + "\n"

        # Main package structure
        p = \
            '%(withs)s'                                 + \
            'package %(package)s\n'                     + \
            'is\n'                                      + \
            '%(constants)s'                             + \
            '%(enums)s'                                 + \
            '%(record)s'                                + \
            '%(constructors)s'                           + \
            '%(ops)s'                                   + \
            'end %(package)s;\n'

        return p % { 'withs':       withs,
                     'package':     ".".join([self.ConvertName(name) for name in self.FullyQualifiedName()]),
                     'constants':   constants,
                     'enums':       enums,
                     'record':      class_record,
                     'constructors': "".join(constructors),
                     'ops':         ops }
