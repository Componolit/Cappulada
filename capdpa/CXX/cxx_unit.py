# Common base class for namespace and class, as the serialization
# is very similar and should be unified.

import cxx

class Unit(cxx.Base):

    def __init__(self, name, constants, enums, used_packages):
        super(Unit, self).__init__()
        self.name          = name
        self.constants     = constants or []
        self.enums         = enums or []
        self.used_packages = used_packages;

    def SerializeHeader(self):

        package   = self.name.PackageFullName()

        # Generate with statements
        withs = ""
        for w in self.used_packages:
            withs += "with " + w + ";\n"
        if withs:
            withs += "\n"

        header = \
            '%(with)s'                                  + \
            'package %(package)s\n'                     + \
            'is\n'

        return header % { 'with':    withs,
                          'package': package }

    def SerializeFooter(self):
        footer = \
            'end %(package)s;\n'

        return footer % { 'package': self.name.PackageFullName() }
