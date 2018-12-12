class Name:

    def __init__ (self, name, entity, pointer, constant, reference):

        # Strip off package namespace, as this is only known internally
        self.name = name[1:]

        self.entity = entity
        self.pointer = pointer
        self.constant = constant
        self.reference = reference

        # Defined here:
        # https://itanium-cxx-abi.github.io/cxx-abi/abi.html#mangling-builtin
        self.builtins = {
            'void':                  "v",
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

    def is_builtin (self):

        return len(self.name) == 0 and self.entity in self.builtins

    def substitution (self):
        return self.builtins[self.entity]

class Namedb:

    def __init__ (self):

        self.db = []

    def Query (self, name):

        result = ""

        # Find longest match in database
        last = len(name.name)
        while not name.name[0:last] in self.db and last > 0:
            last -= 1

        if last > 0:
            index = self.db.index (name.name[0:last])
            tag   = str(index - 1) if index > 0 else ""
            result += "S" + tag + "_"

        # Add new names to db
        for i in range(1, len(name.name) + 1):
            if not name.name[0:i] in self.db:
                self.db.append (name.name[0:i])

        return (result, name.name[last:])

    def Get (self, name, entity, pointer=0, constant=False, reference=False):

        result = ""
        prefix = ""

        name = Name (name, entity, pointer, constant, reference)

        # C_Address actually means void* which we mangle as a pointer 'P' and
        # a builtin type 'v'. FIXME: Wouldn't it be better to actually set
        # self.pointer and a 'void' type in capdpa/cxx.py?
        prefix += "P" if pointer > 0 or entity == "C_Address" else ""
        prefix += "K" if constant else ""
        prefix += "R" if reference else ""

        if name.is_builtin():
            result += name.substitution()
        else:
            (symbol, remainder) = self.Query (name)
            result += symbol

            # Handle all other parts as normal
            for i in remainder:
                result += str(len(i)) + i

            if not entity or entity == "Class":
                pass
            elif entity == "__constructor__":
                result += "C1"
            else:
                result += str(len(entity)) + entity

            # All elements of name have been replaced by reference
            fully_compressed = not remainder

            # At least one component and not fully compressed name
            nested = (symbol or entity) and not fully_compressed

            if nested:
                result = "N" + result + "E"

        return "{prefix}{result}".format(prefix = prefix, result  = result)
