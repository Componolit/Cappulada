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

    def AdaSpecification(self):
        package = ""
        first = True
        for part in self.name:
            name = self.ConvertIdentifier(part)
            package = package + ("." + name if not first else name)
            first = False
        type_name=(self.ConvertIdentifier(self.name[-1]))

        if self.members:
            class_record = "record\n"
            for member in self.members:
                class_record += \
                    "      %(name)s : %(type)s;\n" % \
                    { 'name': self.ConvertIdentifier(member.name),
                      'type': self.ConvertType(member.ctype) }
            class_record += "   end record"
        else:
            class_record = "null record"

        # Main package structure
        p = \
            'package %(package)s\n'                     + \
            'is\n'                                      + \
            '   type %(type)s is\n'                     + \
            '   tagged %(record)s;\n'                   + \
            '   function Constructor return %(type)s\n' + \
            '   with Import => "%(symbol)s";\n'         + \
            'end %(package)s;\n'

        return p % { 'package': package,
                     'type':    type_name,
                     'record':  class_record,
                     'symbol':  self.constructor.symbol }
