import cxx

class NotImplemented(Exception):

    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Class(cxx.Base):

    def __init__(self, name, constructor=None, members=None, functions=None, constants=None, enums=None):

        super(Class, self).__init__()
        self.name        = name
        self.constructor = constructor
        self.members     = members or []
        self.functions   = functions or []
        self.constants   = constants or []
        self.enums       = enums or []

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
            if not t.name.PackagePath() or t.name.PackagePath() == self.name.PackageFull():
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
        constructor = ""
        ops = ""

        if self.constructor:
            # Generate record members
            class_record = '   type %(type)s is\n   tagged ' \
                % { 'type': self.name.PackageBaseName() }
            if self.members:
                class_record += "record\n"
                for member in self.members:
                    class_record += "      " + member.AdaSpecification() + ";\n"
                class_record += "   end record;\n"
            else:
                class_record += "null record;\n"

            # generate constructor
            constructor = \
                ('   function Constructor return %(type)s\n' +
                 '   with Import => "%(symbol)s";\n') \
                    % { 'type':   self.name.PackageBaseName(),
                        'symbol': self.constructor.symbol }

            # generate primitive operations for tagged type
            ops=""
            if self.functions:
                for f in self.functions:
                    ops += "   " + f.AdaSpecification()

        enums = ""

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
            '%(constructor)s'                           + \
            '%(ops)s'                                   + \
            'end %(package)s;\n'

        return p % { 'withs':       withs,
                     'package':     self.name.PackageFullName(),
                     'constants':   constants,
                     'enums':       enums,
                     'record':      class_record,
                     'constructor': constructor,
                     'ops':         ops }
