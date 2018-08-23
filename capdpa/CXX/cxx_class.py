import cxx

class NotImplemented(Exception):

    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Class(cxx.Base):

    def __init__(self, name, constructor=None, members=None, functions=None):
        super(Class, self).__init__()
        self.name        = name
        self.constructor = constructor
        self.members     = members or []
        self.functions   = functions or []

    def UsedPackages(self):
        types = []
        for f in self.functions:
            for p in f.parameters:
                types.append(p.ctype)
                if f.return_type:
                    types.append(f.return_type)

        for m in self.members:
            types.append(m.ctype)

        result = set()
        for t in types:
            # Local varialbe or fully quallified local type, no package needed
            if not t.name.PackagePath() or t.name.PackagePath() == self.name.PackageFull():
                continue
            result.add(t.name.PackagePathName())
        return sorted(list(result))

    def AdaSpecification(self):
        package   = self.name.PackageFullName()
        type_name = self.name.PackageBaseName()

        # Generate with statements
        withs = ""
        for w in self.UsedPackages():
            withs += "with " + w + ";\n"
        if withs:
            withs += "\n"

        # Generate record members
        if self.members:
            class_record = "record\n"
            for member in self.members:
                class_record += "      " + member.AdaSpecification() + ";\n"
            class_record += "   end record"
        else:
            class_record = "null record"

        # generate primitive operations for tagged type
        ops=""
        if self.functions:
            for f in self.functions:
                ops += "   " + f.AdaSpecification()

        # Main package structure
        p = \
            '%(with)s'                                  + \
            'package %(package)s\n'                     + \
            'is\n'                                      + \
            '   type %(type)s is\n'                     + \
            '   tagged %(record)s;\n'                   + \
            '   function Constructor return %(type)s\n' + \
            '   with Import => "%(symbol)s";\n'         + \
            '%(ops)s'                                   + \
            'end %(package)s;\n'

        return p % { 'with':    withs,
                     'package': package,
                     'type':    type_name,
                     'record':  class_record,
                     'ops':     ops,
                     'symbol':  self.constructor.symbol }
