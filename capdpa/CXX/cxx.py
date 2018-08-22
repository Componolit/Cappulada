Keywords = ["abort", "else", "new", "return", "abs", "elsif", "not", "reverse", "abstract", "end", "null", "accept", "entry", "select", "access", "exception", "of", "separate", "aliased", "exit", "or", "some", "all", "others", "subtype", "and", "for", "out", "synchronized", "array", "function", "overriding", "at", "tagged", "generic", "package", "task", "begin", "goto", "pragma", "terminate", "body", "private", "then", "if", "procedure", "type", "case", "in", "protected", "constant", "interface", "until", "is", "raise", "use", "declare", "range", "delay", "limited", "record", "when", "delta", "loop", "rem", "while", "digits", "renames", "with", "do", "mod", "requeue", "xor"]

class NoSerializationDefined: pass

class Base(object):

    def __init__(self): pass

    def ConvertIdentifier(self, identifier):

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

    def ConvertType(self, name):
        return '.'.join(map(self.ConvertIdentifier,name))

    def AdaSpecification(self):
	raise NoSerializationDefined
