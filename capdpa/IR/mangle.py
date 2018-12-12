class Namedb:

    def __init__ (self):

        self.db = []

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

    def Query (self, name):

        index = self.db.index (name)
        tag   = str(index - 1) if index > 0 else ""
        return "S" + tag + "_"

    def Get (self, name, entity, pointer=0, constant=False, reference=False):

        last = 0
        result = ""
        prefix = ""

        # Strip off package namespace, as this is only known internally
        stripped = name[1:]

        # C_Address actually means void* which we mangle as a pointer 'P' and
        # a builtin type 'v'. FIXME: Wouldn't it be better to actually set
        # self.pointer and a 'void' type in capdpa/cxx.py?
        prefix += "P" if pointer > 0 or entity == "C_Address" else ""
        prefix += "K" if constant else ""
        prefix += "R" if reference else ""

        if len(stripped) == 0 and entity in self.builtins:
            result += self.builtins[entity]
        else:
            # Find longest match in database
            last = len(stripped)
            while not stripped[0:last] in self.db and last > 0:
                last -= 1

            if last > 0:
                result += self.Query (stripped[0:last])

            # Add new names to db
            for i in range(1, len(stripped) + 1):
                if not stripped[0:i] in self.db:
                    self.db.append (stripped[0:i])

            # Handle all other parts as normal
            for i in stripped[last:]:
                result += str(len(i)) + i

            if not entity or entity == "Class":
                pass
            elif entity == "__constructor__":
                result += "C1"
            else:
                result += str(len(entity)) + entity

            # All elements of name have been replaced by reference
            fully_compressed = last > 0 and last == len(stripped)

            # At least one component and not fully compressed name
            nested = (len(stripped) > 1 or entity) and not fully_compressed

            if nested:
                result = "N" + result + "E"

        return "{prefix}{result}".format(prefix = prefix, result  = result)
