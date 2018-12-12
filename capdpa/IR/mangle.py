class Name:

    def __init__ (self, name, entity, pointer, constant, reference):

        # Strip off package namespace, as this is only known internally
        self.name = name[1:]

        self.entity = entity
        self.pointer = pointer > 0
        self.constant = constant
        self.reference = reference

        # Defined here:
        # https://itanium-cxx-abi.github.io/cxx-abi/abi.html#mangling-builtin
        self.builtins = {
            'void':                  'v',
            'wchar_t':               'w',
            'bool':                  'b',
            'char':                  'c',
            'signed_char':           'c',  # GCC disagrees with spec (which says 'a')
            'unsigned_char':         'h',
            'short':                 's',
            'unsigned_short':        't',
            'int':                   'i',
            'unsigned_int':          'j',
            'long':                  'l',
            'unsigned_long':         'm',
            'long_long':             'x',
            'unsigned_long_long':    'y',
            '__int128':              'n',
            'unsigned___int128':     'o',
            'float':                 'f',
            'double':                'd',
            'long_double':           'e',
            '__float128':            'g',
            'C_Address':             'v',
        }

    def __repr__ (self):
        return ".".join(self.name + [self.entity] if self.entity else []) + ": pointer=" + str(self.pointer) + " constant=" + str(self.constant) + " reference=" + str(self.reference)

    def is_builtin (self):

        return len(self.name) == 0 and self.entity in self.builtins

    def prefix (self):

        result = ""

        # C_Address actually means void* which we mangle as a pointer 'P' and
        # a builtin type 'v'. FIXME: Wouldn't it be better to actually set
        # self.pointer and a 'void' type in capdpa/cxx.py?
        result += "P" if self.pointer or self.entity == "C_Address" else ""
        result += "K" if self.constant else ""
        result += "R" if self.reference else ""

        return result

    def substitution (self):
        return self.builtins[self.entity]

class Namedb:

    def __init__ (self):

        self.db = []

    def Query (self, name):

        result = ""

        if name.is_builtin():
            return (name.substitution(), False)

        # Find longest match in database
        last = len(name.name)
        while last > 0 and not (name.name[0:last], name.pointer, name.constant, name.reference) in self.db:
            last -= 1

        # Found a match
        if last > 0:
            index = self.db.index ((name.name[0:last], name.pointer, name.constant, name.reference))
            tag   = str(index - 1) if index > 0 else ""
            result += "S" + tag + "_"

        # Add new names to db
        for i in range(1, len(name.name) + 1):
            new = (name.name[0:i], name.pointer, name.constant, name.reference)
            if not new in self.db:
                self.db.append (new)

        if last == 0:
            const = (name.name, False, True, False)
            if name.constant and not const in self.db:
                self.db.append (const)

        # Handle all other parts as normal
        for i in name.name[last:]:
            result += str(len(i)) + i

        if not name.entity or name.entity == "Class" or name.is_builtin():
            pass
        elif name.entity == "__constructor__":
            result += "C1"
        else:
            result += str(len(name.entity)) + name.entity

        # At least one component and not fully compressed name
        nested = (len(name.name) > 1 or name.entity) and last != len(name.name)
        return (result, nested)

    def Get (self, name, entity, pointer=False, constant=False, reference=False):

        # Query name in database
        n = Name (name, entity, pointer, constant, reference)
        (result, nested) = self.Query (n)

        if nested:
            result = "N" + result + "E"
        return n.prefix() + result
