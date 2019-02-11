Keywords = ["abort", "else", "new", "return", "abs", "elsif", "not", "reverse",
            "abstract", "end", "null", "accept", "entry", "select", "access",
            "exception", "of", "separate", "aliased", "exit", "or", "some",
            "all", "others", "subtype", "and", "for", "out", "synchronized",
            "array", "function", "overriding", "at", "tagged", "generic",
            "package", "task", "begin", "goto", "pragma", "terminate", "body",
            "private", "then", "if", "procedure", "type", "case", "in",
            "protected", "constant", "interface", "until", "is", "raise",
            "use", "declare", "range", "delay", "limited", "record", "when",
            "delta", "loop", "rem", "while", "digits", "renames", "with", "do",
            "mod", "requeue", "xor"]

class NotImplemented(Exception):
    def __init__(self, message):
        super(NotImplemented, self).__init__(message);

class Base(object):

    parent = None

    def __init__(self): pass

    def __eq__(self, other):
        return self.__repr__() == repr(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self, ignores=None):
        ignorelist = ['parent']
        if ignores:
            ignorelist.extend(ignores)
        return "{}({})".format(
                self.__class__.__name__,
                ",".join("{}={}".format(k, v) for k,v in sorted(self.__dict__.items()) if k not in ignorelist))

    def __hash__(self):
        return hash(self.__repr__())

    def __getitem__(self, arg):
        if hasattr(self, "children"):
            if isinstance(arg, list):
                return self.__getitem__(tuple(arg))
            elif isinstance(arg, tuple):
                if len(arg) > 1:
                    return self[arg[0]][arg[1:]]
                else:
                    return self[arg[0]]
            else:
                for c in self.children:
                    if c.name == arg:
                        return c
                else:
                    raise KeyError(arg)

    def __contains__(self, arg):
        if hasattr(self, "children"):
            if isinstance(arg, list):
                return self.__contains__(tuple(arg))
            elif isinstance(arg, tuple):
                if len(arg) > 1:
                    if arg[0] in self:
                        return arg[1:] in self[arg[0]]
                else:
                    return arg[0] in self
            else:
                for c in self.children:
                    if c.name == arg:
                        return True
                else:
                    return False

    def _parentize_list(self, children):
        map(lambda c: c.SetParent(self), children)

    @classmethod
    def isInst(cls, obj):
        return isinstance(obj, cls)

    def SetParent(self, parent):
        self.parent = parent

    def GetRoot(self):
        parent = self.parent
        if parent:
            while parent.parent:
                parent = parent.parent
            return parent
        else:
            return self

    def InstantiateTemplates(self):
        for c in self.children:
            c.InstantiateTemplates()

    def UsedTypes(self, parent=None):
        types = []
        for c in self.children:
            types.extend (c.UsedTypes(parent))
        return types

    def FullyQualifiedName(self):
        if self.parent:
            fqn = self.parent.FullyQualifiedName()
            fqn.append(self.name)
            return fqn
        else:
            return [self.name]

    def PackagePath(self):
        return self.name.name[:-1]

    def PackageName(self):
        return ".".join(map(self.ConvertName, self.PackagePath()))


    def isVirtual(self):
        return False

    def ConvertName(self, identifier):

        result = identifier.lower()
        digit  = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        letter = map (chr, range(ord('a'), ord('z')+1))
        underscore = ['_']

        # Ada identifier grammar:
        #
        # identifier ::= letter { [ underscore ] letter | digit }
        # letter ::= A | ... | Z | a | ... | z
        # digit ::= 0 | ... | 9
        # underscore ::= _
        #
        # Also, keywords must be excluded.

        tmp = ""
        is_first = True;
        was_underscore = False
        for c in result:
            # Replace unsupported characters by its ord in hex
            if not c in digit + letter + underscore:
                tmp = tmp + hex(ord(c))[2:]
            else:
                if c == '_' and was_underscore:
                    tmp = tmp + "X"
                if is_first or was_underscore:
                    tmp = tmp + c.upper()
                else:
                    tmp = tmp + c
            was_underscore = c == '_'
            is_first = False

        # Handle leading underscore
        if tmp[0] in digit or tmp[0] in underscore:
            tmp = "X" + tmp

        # Handle trailing underscore
        if tmp[-1] in underscore:
            tmp = tmp + "X"

        if tmp.lower() in Keywords:
            tmp = "X_" + tmp

        return tmp

    def AdaSpecification(self, indentation=0, **kwargs):
	raise NotImplemented("No specification defined for " + type(self).__name__)

    def Mangle(self):
	raise NotImplemented("No mangling defined for " + type(self).__name__)
