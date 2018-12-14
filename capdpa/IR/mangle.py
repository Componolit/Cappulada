from numpy import base_repr

# Defined here: # https://itanium-cxx-abi.github.io/cxx-abi/abi.html#mangling-builtin
builtins = {
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
}

class Base(object):

    def __init__ (self, obj):
        self.obj = obj

    def __str__ (self):
        namedb = DB("Namedb")
        return self.serialize(namedb, True)

    def __len__ (self):
        return 1 + len(self.obj)

    def serialize (self, namedb, subst):
        raise Exception ("Not implemented")

class Type (Base):

    def __init__ (self, name):
        self.name = Nested (Name (name))

    def serialize (self, namedb, subst):
        return self.name.serialize(namedb, subst)

class Pointer (Base):

    def serialize (self, namedb, subst):

        result = "P" + self.obj.serialize (namedb, False)
        if not subst:
            return result

        if namedb.contains (result):
            result = namedb.substitute (result)
        else:
            result = "P" + self.obj.serialize (namedb, True)
            namedb.insert (result)

        return result

class Reference (Base):

    def serialize (self, namedb, subst):

        result = "R" + self.obj.serialize (namedb, False)
        if not subst:
            return result

        if namedb.contains (result):
            result = namedb.substitute (result)
        else:
            result = "R" + self.obj.serialize (namedb, True)
            namedb.insert (result)

        return result

class Constant (Base):

    def serialize (self, namedb, subst):

        result = "K" + self.obj.serialize(namedb, False)
        if not subst:
            return result

        if namedb.contains (result):
            result = namedb.substitute (result)
        else:
            result = "K" + self.obj.serialize(namedb, True)
            namedb.insert (result)

        return result

class Constructor (Base):

    def serialize (self, namedb, subst):
        return self.obj.serialize(namedb, subst) + "C1"

class Name (Base):

    def __init__ (self, name, entity = None):
        obj = None
        for n in name:
            obj = Names(n, obj)
        self.obj = Entity (obj, entity)

    def __len__ (self):
        return len(self.obj)

    def serialize (self, namedb, subst):
        return self.obj.serialize (namedb, subst)

class Names (Base):

    def __init__ (self, name, obj):
        self.name = name
        self.obj = obj

    def __len__ (self):
        return 1 + (len(self.obj) if self.obj else 0)

    def serialize (self, namedb, subst):

        if self.name in builtins:
            return builtins[self.name]

        result = str(len(self.name)) + self.name

        unsubst = result
        if self.obj:
            unsubst = self.obj.serialize(namedb, False) + unsubst

        if not subst:
            return unsubst

        if self.obj:
            result = self.obj.serialize(namedb, True) + result

        if namedb.contains (unsubst):
            return namedb.substitute (unsubst)
        namedb.insert (unsubst)
        return result

class Entity (Base):

    def __init__ (self, obj, name):
        self.obj = obj
        self.name = name

    def __len__ (self):
        l = 1 if self.name else 0
        return l + len(self.obj)

    def serialize (self, namedb, subst):

        result = self.obj.serialize(namedb, subst)
        if self.name:
            result += str(len(self.name)) + self.name
        return result

class Symbol (Base):

    def serialize (self, namedb, subst):

        result = ""
        for o in self.obj:
            result += o.serialize(namedb, subst)
        return "_Z" + result

class Nested (Base):

    def serialize (self, namedb, subst):

        name = self.obj.serialize(namedb, subst)
        if len(self.obj) > 1 and not namedb.index (name[1:-1]):
            return "N" + name + "E"
        else:
            return name

class Function (Base):

    def __init__ (self, name, obj):
        self.name = name
        self.obj = obj

    def serialize (self, namedb, subst):

        result = "F" + self.name.serialize(namedb, False)
        for o in self.obj:
            result += o.serialize(namedb, False)
        result += "E"

        if not subst:
            return result

        if namedb.contains (result):
            result = namedb.substitute (result)
        else:
            result = "F" + self.name.serialize(namedb, True)
            for o in self.obj:
                result += o.serialize(namedb, True)
            result += "E"
            namedb.insert (result)

        return result

class Template (Base):

    def __init__ (self, name, obj):
        self.name = name
        self.obj = obj

    def serialize (self, namedb, subst):

        result = ""
        for o in self.obj:
            result += o.serialize(namedb, subst)

        return self.name.serialize(namedb, subst) + "I" + result + "E"

class DB:
    def __init__ (self, name):

        self.db = []
        self.name = name

    def __repr__ (self):
        return "DB " + str(self.name) + ": " + "[" + ", ".join ([self.tag (self.db.index (x)) + "=" + x for x in self.db]) + "]"

    def insert (self, name):
        if not name in self.db:
            self.db.append (name)

    def contains (self, name):
        return name in self.db

    def tag (self, index):
        return "S" + (base_repr(index - 1, 36).lower() if index > 0 else "") + "_"

    def index (self, name):
        try:
            i = int(name, 36)
        except:
            return None

        if i < len(self.db):
            return self.db[i]
        return None

    def substitute (self, name):
        index = self.db.index (name)
        return self.tag (index)
