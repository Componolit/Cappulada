import cxx
import cxx_unit

class NotImplemented(Exception):

    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Class(cxx_unit.Unit):

    def __init__(self, name, constructor=None, members=None, functions=None, constants=None, enums=None):

        self.constructor = constructor
        self.members     = members or []
        self.functions   = functions or []

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
            if not t.name.PackagePath() or t.name.PackagePath() == name.PackageFull():
                continue
            used_packages.add(t.name.PackagePathName())

        super(Class, self).__init__(name, constants, enums, sorted(list(used_packages)))

    def AdaSpecification(self):

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
            '%(header)s'                                + \
            '   type %(type)s is\n'                     + \
            '   tagged %(record)s;\n'                   + \
            '   function Constructor return %(type)s\n' + \
            '   with Import => "%(symbol)s";\n'         + \
            '%(ops)s'                                   + \
            '%(footer)s'

        return p % { 'header':  self.SerializeHeader(),
                     'type':    self.name.PackageBaseName(),
                     'record':  class_record,
                     'ops':     ops,
                     'symbol':  self.constructor.symbol,
                     'footer':  self.SerializeFooter() }
