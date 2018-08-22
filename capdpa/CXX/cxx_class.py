import cxx

class NotImplemented(Exception):

    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Class(cxx.Base):

    def __init__(self, name, constructor=None, members=None, functions=None):
        super(Class, self).__init__()
        self.name = name
        self.constructor = constructor
        self.members = members or []
        self.functions = functions or []

    def UsedPackages(self):
        if self.functions:
            raise NotImplmented("Type handling for function parameters")
        result = set()
        for m in self.members:
            # Local type, no package needed
            if len(m.ctype) <= 1:
                continue
            result.add(".".join(map(self.ConvertIdentifier, m.ctype[:-1])))
        return sorted(list(result))

    def AdaSpecification(self):
        package = ""
        first = True
        for part in self.name:
            name = self.ConvertIdentifier(part)
            package += ("." + name if not first else name)
            first = False
        type_name=(self.ConvertIdentifier(self.name[-1]))

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
                class_record += "      " + member.AdaSpecification() + "\n"
            class_record += "   end record"
        else:
            class_record = "null record"

        # Main package structure
        p = \
            '%(with)s'                                  + \
            'package %(package)s\n'                     + \
            'is\n'                                      + \
            '   type %(type)s is\n'                     + \
            '   tagged %(record)s;\n'                   + \
            '   function Constructor return %(type)s\n' + \
            '   with Import => "%(symbol)s";\n'         + \
            'end %(package)s;\n'

        return p % { 'with':    withs,
                     'package': package,
                     'type':    type_name,
                     'record':  class_record,
                     'symbol':  self.constructor.symbol }
