import ir
import ir_type
import ir_identifier
import mangle

class Function(ir.Base):

    def __init__(self, name, parameters=None, return_type=None, virtual=False, static=False):
        super(Function, self).__init__()
        self.name = name
        self.parameters = parameters or []
        self._parentize_list(self.parameters)
        self.return_type = return_type
        if self.return_type:
            self.return_type.parent = self
        self.virtual = virtual
        self.static = static

    def isVirtual(self):
        return self.virtual

    def AdaSpecification(self, indentation=0):

        result = " " * indentation + ("function " if self.return_type else "procedure ")
        result += self.ConvertName(self.name)

        result += " ("
        first = self.static
        if not self.static:
            result += "This : access Class"

        if self.parameters:
            for p in self.parameters:
                if not first:
                    result += "; "
                first = False
                result += p.AdaSpecification()
        result += ")"

        result += (" return " + self.return_type.AdaSpecification() + "\n") if self.return_type else "\n"
        result += " " * indentation + 'with Import, Convention => CPP, External_Name => "' + str(self.Mangle ()) + '";\n'

        return result

    def InstantiateTemplates(self):
        for p in self.parameters:
            p.InstantiateTemplates()
        #TODO: return_code templates

    def Mangle(self):
        return self.Mangle_Function(False)

    def Mangle_Function(self, constructor):

        if not self.parent:
            raise Exception ("Parent not set")

        entity = mangle.Literal("C1") if constructor else mangle.String(self.name)

        if not self.parent.instanceof:
            # Regular class
            name = mangle.Name ([mangle.String(n) for n in self.parent.FullyQualifiedName()[1:]], entity)
        else:
            # Template
            (template_name, template_args) = self.parent.instanceof
            basename = [mangle.String(n) for n in template_name[1:]]
            args = mangle.Template ([mangle.Type ([mangle.String(x) for x in t.name.name[1:]]) for t in template_args])
            name = mangle.Name (basename + [args], entity)

        parameters = [p.Mangle() for p in self.parameters] if self.parameters else [mangle.Type ([mangle.String("void")])]
        return mangle.Symbol ([mangle.Nested (name)] + parameters)

class Function_Reference(Function):

    def __init__(self, parameters=None, return_type=None, pointer=1, reference=False, static=False):
        super(Function_Reference, self).__init__(name="", parameters=parameters, return_type=return_type, virtual=False, static=static)
        self.name = ir_identifier.Identifier([])
        self.pointer = pointer
        self.reference = reference

        if self.pointer == 0 and not self.reference:
            raise Exception ("Invalid function reference (neither ref nor pointer)")

    def AdaSpecification(self, indentation=0, private=""):
        if private == "":
            first = self.static

            args = " ("
            if not self.static:
                args += "This : access Class"

            for p in self.parameters:
                if not first:
                    args += "; "
                first = False
                args += p.AdaSpecification()
            args += ")"

            kind   = "function" if self.return_type else "procedure"
            ret    = " return {}".format(self.return_type.AdaSpecification()) if self.return_type else ""
            name   = "access " + kind + args + ret
        else:
            name = "Private_Procedure"
        return " " * indentation + name

    def Mangle(self):

        # return type
        if self.return_type:
            return_type = self.return_type.Mangle ()
        else:
            return_type = mangle.Type ([mangle.String("void")])

        # parameters
        parameters = []
        if self.parameters:
            for p in self.parameters:
                parameters.append (p.Mangle ())
        else:
            parameters.append (mangle.Type ([mangle.String("void")]))

        result = mangle.Function (return_type, parameters)

        if self.reference:
            result = mangle.Reference (result)

        if self.pointer:
            result = mangle.Pointer (result)

        return result

class Constructor(Function):

    def __init__(self, parameters=None):
        super(Constructor, self).__init__("__constructor__", parameters, None)
        self.parameters = parameters or []

    def __repr__(self):
        return "Constructor(parameters={})".format(self.parameters)

    def AdaSpecification(self, indentation=0):
        return "{0}function Constructor{1} return Class;\n{0}pragma Cpp_Constructor (Constructor, \"{2}\");\n".format(
                " " * indentation,
                " ({})".format("; ".join(
                    map(lambda p: p.AdaSpecification(), self.parameters))) if self.parameters else "", str(self.Mangle ()))

    def Mangle(self):
        return super(Constructor, self).Mangle_Function(True)
