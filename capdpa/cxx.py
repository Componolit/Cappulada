
import clang.cindex
import IR
import cymbal
import ctypes

cymbal.monkeypatch_type(
        'get_template_argument_type',
        'clang_Type_getTemplateArgumentAsType',
        [clang.cindex.Type, ctypes.c_uint],
        clang.cindex.Type)

cymbal.monkeypatch_type(
        'get_num_template_arguments',
        'clang_Type_getNumTemplateArguments',
        [clang.cindex.Type],
        ctypes.c_int)

class InvalidNodeError: pass

TypeMap = {
        clang.cindex.TypeKind.BOOL      : "bool",
        clang.cindex.TypeKind.CHAR_U    : "unsigned_char",
        clang.cindex.TypeKind.UCHAR     : "unsigned_char",
        clang.cindex.TypeKind.USHORT    : "unsigned_short",
        clang.cindex.TypeKind.UINT      : "unsigned_int",
        clang.cindex.TypeKind.ULONG     : "unsigned_long",
        clang.cindex.TypeKind.ULONGLONG : "unsigned_long_long",
        clang.cindex.TypeKind.CHAR_S    : "char",
        clang.cindex.TypeKind.SCHAR     : "signed_char",
        clang.cindex.TypeKind.WCHAR     : "wchar_t",
        clang.cindex.TypeKind.SHORT     : "short",
        clang.cindex.TypeKind.INT       : "int",
        clang.cindex.TypeKind.INT128    : "C__int128",
        clang.cindex.TypeKind.UINT128   : "unsigned___int128",
        clang.cindex.TypeKind.LONG      : "long",
        clang.cindex.TypeKind.LONGLONG  : "long_long",
        clang.cindex.TypeKind.FLOAT     : "C_float",
        clang.cindex.TypeKind.DOUBLE    : "double",
        clang.cindex.TypeKind.LONGDOUBLE: "long_double"
        }

class CXX:

    class ParseError(Exception):
        def __init__(self, error):
            self.error = error
            self.message = ""
            for d in self.error:
                self.message += str(d.location.file) + ":" + str(d.location.line) + ":" + str(d.location.column) +  ": " + d.spelling + "\n"

        def __str__(self):
            return self.message

    class LoadError(Exception):
        def __init__(self, error, header):
            self.error = error
            self.header = header

        def __str__(self):
            return self.header + ": " + str(self.error)

    def __init__(self, header, flags = []):
        try:
            self.index = clang.cindex.Index.create()
            self.translation_unit = self.index.parse(header, ["-x", "c++", "-std=c++14", "-Wno-attributes"] + flags)
            if self.translation_unit.diagnostics:
                for diag in self.translation_unit.diagnostics:
                    if diag.severity > 0:
                       raise CXX.ParseError(self.translation_unit.diagnostics)
        except clang.cindex.TranslationUnitLoadError as e:
            raise CXX.LoadError(e, header)

    def __print_layer(self, cursor):
        print(str(cursor.kind) + " (" + cursor.displayname + "): " + str([cursor.kind for cursor in cursor.get_children()]))

    def __print_tree(self, cursor, indent):
        print(" " * indent + (cursor.displayname or "UNNAMED") + " (" + str(cursor.kind) + ")")
        for c in cursor.get_children():
            self.__print_tree(c, indent + 2)

    def __convert_class(self, cursor):
        if cursor.kind not in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL]:
            raise InvalidNodeError
        children = cursor.get_children()
        if clang.cindex.CursorKind.TYPE_REF in [c.kind for c in children]:
            #fully specialized template instance, should be generated if used automatically by us
            return None
        else:
            return IR.Class(
                    name = cursor.displayname,
                    children = self.__convert_children(cursor.get_children()),
                    public = cursor.access_specifier in [
                        clang.cindex.AccessSpecifier.PUBLIC,
                        clang.cindex.AccessSpecifier.INVALID])

    def __convert_base(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            raise InvalidNodeError
        return IR.Class_Reference(name=
                IR.Identifier(self.__resolve_name(cursor.type.get_declaration())))

    def __convert_function(self, cursor):
        return IR.Function(
                name = cursor.spelling,
                parameters = self.__convert_arguments(cursor.get_children()),
                return_type = self.__convert_type(list(cursor.get_children()), cursor.result_type))

    def __convert_method(self, cursor):

        ada = True in [x.kind == clang.cindex.CursorKind.ANNOTATE_ATTR and x.spelling == "ada" for x in cursor.get_children()]

        return IR.Method(
                name = cursor.spelling,
                parameters = self.__convert_arguments(cursor.get_children()),
                return_type = self.__convert_type([], cursor.result_type),
                virtual = cursor.is_virtual_method(),
                static = cursor.is_static_method(),
                export = ada)

    def __convert_constructor(self, cursor):
        return IR.Constructor(
                parameters = self.__convert_arguments(cursor.get_children()))

    def __convert_destructor(self, cursor):
        return IR.Destructor()

    def __resolve_name(self, cursor):
        identifier = []
        while cursor and cursor.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            identifier.append(cursor.spelling)
            cursor = cursor.semantic_parent
        return [self.project] + list(reversed(identifier))

    def __convert_type(self, children, type_cursor):
        ptr = 0;
        reference = False;

        while type_cursor.kind == clang.cindex.TypeKind.POINTER:
            ptr += 1
            type_cursor = type_cursor.get_pointee()

        if type_cursor.kind == clang.cindex.TypeKind.LVALUEREFERENCE:
            reference = True
            type_cursor = type_cursor.get_pointee()
        const = type_cursor.is_const_qualified()
        if type_cursor.kind in [clang.cindex.TypeKind.UNEXPOSED, clang.cindex.TypeKind.RECORD] \
                or (type_cursor.kind == clang.cindex.TypeKind.TYPEDEF and len(children) > 0 and children[0].kind == clang.cindex.CursorKind.TEMPLATE_REF):
            targs = type_cursor.get_num_template_arguments()
            decl = type_cursor.get_declaration()
            if targs > 0:
                args = []
                ccursor = 1
                for i in range(targs):
                    cymbal_arg = type_cursor.get_template_argument_type(i)
                    if cymbal_arg.kind in TypeMap.keys():
                        args.append(self.__convert_type(children, cymbal_arg))
                        # only use builtin types from cymbal
                    else:
                        try:
                            child_arg = children[ccursor]
                            ccursor += 1
                            if child_arg.kind in [
                                    clang.cindex.CursorKind.INTEGER_LITERAL,
                                    clang.cindex.CursorKind.FLOATING_LITERAL,
                                    clang.cindex.CursorKind.IMAGINARY_LITERAL,
                                    clang.cindex.CursorKind.STRING_LITERAL,
                                    clang.cindex.CursorKind.CHARACTER_LITERAL,
                                    clang.cindex.CursorKind.CXX_BOOL_LITERAL_EXPR]:
                                if child_arg.type.kind in TypeMap.keys():
                                    args.append(IR.Type_Literal(
                                        name = IR.Identifier([self.project, TypeMap[child_arg.type.kind]]),
                                        value=list(child_arg.get_tokens())[0].spelling.strip("'")))
                                else:
                                    raise NotImplementedError("Literal type conversion not implemented: " + str(child_arg.type.kind))
                            else:
                                args.append(self.__convert_type(children, child_arg.type.get_declaration().type))
                        except IndexError:
                            #FIXME: here we should add an argument to a variadic template but clang doesn't give type information on those args so we can't
                            pass
                if type_cursor.kind == clang.cindex.TypeKind.TYPEDEF:
                    trt_name = self.__resolve_name(list(decl.get_children())[0])
                else:
                    trt_name = self.__resolve_name(decl)
                return IR.Type_Reference_Template(
                        name = IR.Identifier(trt_name),
                        constant = const,
                        arguments = args,
                        pointer = ptr, reference=reference)
            elif decl.kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL]:
                name = self.__resolve_name(decl)
                if decl.access_specifier in [clang.cindex.AccessSpecifier.PUBLIC, clang.cindex.AccessSpecifier.INVALID]:
                    name += ["Class"]
                return IR.Type_Reference(
                        name = IR.Identifier(name),
                        constant = const,
                        pointer = ptr,
                        reference = reference)
            elif decl.kind in [clang.cindex.CursorKind.ENUM_DECL,
                    clang.cindex.CursorKind.TYPEDEF_DECL,
                    clang.cindex.CursorKind.TYPE_ALIAS_DECL]:
                return IR.Type_Reference(
                        name = IR.Identifier(self.__resolve_name(decl)),
                        pointer = ptr,
                        reference = reference)
            elif decl.kind == clang.cindex.CursorKind.NO_DECL_FOUND:
                canon = type_cursor.get_canonical().kind
                if canon == clang.cindex.TypeKind.UNEXPOSED:
                    return IR.Template_Argument(
                        name = type_cursor.spelling,
                        reference = reference,
                        pointer = ptr)
                elif canon == clang.cindex.TypeKind.FUNCTIONPROTO:
                    return IR.Function_Reference(
                        parameters=self.__convert_arguments(children),
                        return_type=self.__convert_type([], type_cursor.get_result()),
                        pointer = ptr,
                        reference = reference)
                else:
                    raise NotImplementedError("Unknown undeclared canonical type: {}".format(canon))
            elif decl.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
                return IR.Type_Reference_Template(name = IR.Identifier(self.__resolve_name(children[0])), arguments=[
                    IR.Template_Argument(name=c.spelling) for c in children[1:]])
            else:
                raise NotImplementedError("Unsupported declaration kind {} at {}".format(decl.kind, decl.location))
        elif type_cursor.kind == clang.cindex.TypeKind.VOID:
            return IR.Type_Reference(
                name = IR.Identifier([self.project, "void"]),
                constant = const,
                pointer = 1,
                reference = reference) if ptr else None
        elif type_cursor.kind == clang.cindex.TypeKind.TYPEDEF:
            return IR.Type_Reference(name = IR.Identifier(
                [type_cursor.spelling]),
                constant = const,
                pointer = ptr,
                reference = reference)
        elif type_cursor.kind == clang.cindex.TypeKind.ENUM:
            return IR.Type_Reference(name = IR.Identifier(
                self.__resolve_name(type_cursor.get_declaration())),
                constant = const,
                pointer = ptr,
                reference=reference)
        elif type_cursor.kind == clang.cindex.TypeKind.MEMBERPOINTER:
            parent_type = type_cursor.get_class_type().kind
            if parent_type == clang.cindex.TypeKind.RECORD:
                return IR.Function_Reference(
                    parameters=self.__convert_arguments(children),
                    return_type=self.__convert_type([], type_cursor.get_result()),
                    pointer = ptr,
                    reference = reference)
            elif parent_type == clang.cindex.TypeKind.UNEXPOSED:
                return IR.Function_Reference(
                    parameters=self.__convert_arguments(children),
                    return_type=self.__convert_type([], type_cursor.get_result()),
                    pointer=1,
                    static=True)
            else:
                raise NotImplementedError("Unsupported type of memberpointer: {}".format(parent_type))
        elif type_cursor.kind == clang.cindex.TypeKind.CONSTANTARRAY:
            return IR.Array(
                    ctype = self.__convert_type(children, type_cursor.element_type),
                    size = type_cursor.element_count)
        elif type_cursor.kind == clang.cindex.TypeKind.DEPENDENTSIZEDARRAY:
            return IR.Array(
                    ctype = self.__convert_type(children, type_cursor.element_type),
                    size = IR.Template_Argument(name = children[0].spelling))
        elif type_cursor.kind == clang.cindex.TypeKind.INCOMPLETEARRAY:
            return IR.Array(
                    ctype = self.__convert_type(children, type_cursor.element_type),
                    size = 0,
                    constrained = False)
        elif type_cursor.kind in TypeMap.keys():
            return IR.Type_Reference(
                name = IR.Identifier([self.project, TypeMap[type_cursor.kind]]),
                constant = const,
                pointer = ptr,
                reference = reference)
        else:
            raise NotImplementedError("Unsupported type: {} (from {})".format(type_cursor.kind, type_cursor.spelling))

    def __convert_arguments(self, cursors):
        argv = []
        argc = 1
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.PARM_DECL:
                ptype = self.__convert_type(list(cursor.get_children()), cursor.type)
                if cursor.displayname:
                    argv.append(IR.Argument(name = cursor.displayname, ctype = ptype))
                else:
                    argv.append(IR.Argument(name = "arg" + str(argc), ctype = ptype))
                argc += 1
        return argv

    def __convert_member(self, cursor):
        return IR.Member(
                name = cursor.displayname,
                ctype = self.__convert_type(list(cursor.get_children()), cursor.type),
                access="public" if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC else "private",
                constant=cursor.type.is_const_qualified())

    def __convert_variable(self, cursor):
        return IR.Variable(
                name = cursor.displayname,
                private = cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE,
                ctype = self.__convert_type(list(cursor.get_children()), cursor.type))

    def __convert_constant(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
            raise InvalidNodeError
        return IR.Constant(
                name = cursor.displayname,
                value = cursor.enum_value)

    def __convert_enum(self, cursor):

        def compare(left, right):
            if left.value < right.value:
                return -1;
            elif left.value > right.value:
                return 0;
            else:
                return 0;

        return IR.Enum(
            name = cursor.displayname,
            children = sorted([self.__convert_constant(constant) for constant in cursor.get_children()], cmp=compare),
            ctype = self.__convert_type([], cursor.enum_type))

    def __convert_namespace(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.NAMESPACE:
            raise InvalidNodeError
        return IR.Namespace(
                name = cursor.displayname,
                children = self.__convert_children(cursor.get_children())
                )

    def __convert_typedef(self, cursor):
        children = list(cursor.get_children())
        if children:
            if children[0].kind in [
                    clang.cindex.CursorKind.TEMPLATE_REF,
                    clang.cindex.CursorKind.NAMESPACE_REF]:
                resolved = self.__convert_type(children, cursor.type)
            elif children[0].kind in [
                    clang.cindex.CursorKind.TYPE_REF]:
                resolved = self.__convert_type([], children[0].type)
            else:
                resolved = self.__convert_type(children, cursor.type.get_canonical())
        else:
            resolved = self.__convert_type([], cursor.type.get_canonical())
        return IR.Type_Definition(cursor.type.spelling, resolved)

    def __convert_template(self, cursor):
        targs = []
        for c in cursor.get_children():
            if c.kind in [
                    clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER,
                    clang.cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER]:
                targs.append(c)
        return IR.Template(
                entity = IR.Class(
                    name = cursor.spelling,
                    children = self.__convert_children(list(cursor.get_children())[len(targs):]),
                    public = cursor.access_specifier in [
                        clang.cindex.AccessSpecifier.INVALID,
                        clang.cindex.AccessSpecifier.PUBLIC]),
                typenames = [IR.Template_Argument(name = c.spelling,
                                                  variadic = list(c.get_tokens())[1].spelling == "...") for c in targs])


    def __convert_children(self, cursors):
        children = []
        clist = list(cursors)
        for cursor in clist:
            if cursor.access_specifier in [clang.cindex.AccessSpecifier.PUBLIC, clang.cindex.AccessSpecifier.INVALID]:
                if cursor.semantic_parent and \
                   cursor.semantic_parent.kind == clang.cindex.CursorKind.CLASS_DECL and \
                   cursor.lexical_parent and \
                   cursor.lexical_parent != cursor.semantic_parent:
                    # Filter out method definitions outside the class declaration
                    pass
                elif cursor.kind == clang.cindex.CursorKind.NAMESPACE:
                    children.append(self.__convert_namespace(cursor))
                elif cursor.kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL]:
                    decl = self.__convert_class(cursor)
                    if decl and True not in [c.name == decl.name for c in children]:
                        if not cursor.is_definition():
                            if cursor.get_definition() and cursor.get_definition() in clist:
                                definition = cursor.get_definition()
                                decl = self.__convert_class(definition)
                                if decl:
                                    children.append(decl)
                            else:
                                children.append(IR.Type_Definition(decl.name, None))
                        else:
                            children.append(decl)
                elif cursor.kind == clang.cindex.CursorKind.ENUM_DECL:
                    if cursor.displayname:
                        children.append(self.__convert_enum(cursor))
                    else:
                        [children.append(self.__convert_constant(constant)) for constant in cursor.get_children()]
                elif cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
                    children.append(self.__convert_method(cursor))
                elif cursor.kind in [
                        clang.cindex.CursorKind.TYPEDEF_DECL,
                        clang.cindex.CursorKind.TYPE_ALIAS_DECL]:
                    children.append(self.__convert_typedef(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CONSTRUCTOR:
                    children.append(self.__convert_constructor(cursor))
                elif cursor.kind == clang.cindex.CursorKind.DESTRUCTOR:
                    children.append(self.__convert_destructor(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
                    children.append(self.__convert_template(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
                    children.append(self.__convert_base(cursor))
                elif cursor.kind == clang.cindex.CursorKind.FIELD_DECL:
                    children.append(self.__convert_member(cursor))
                elif cursor.kind == clang.cindex.CursorKind.VAR_DECL:
                    children.append(self.__convert_variable(cursor))
                elif cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                    children.append(self.__convert_function(cursor))
                elif cursor.kind in [
                        clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL,
                        clang.cindex.CursorKind.UNEXPOSED_DECL,
                        clang.cindex.CursorKind.NAMESPACE_REF,
                        clang.cindex.CursorKind.TEMPLATE_REF,
                        clang.cindex.CursorKind.FUNCTION_TEMPLATE,
                        # TODO: properly support function templates
                        clang.cindex.CursorKind.CONVERSION_FUNCTION,
                        # Just ignore c++ conversion operators
                        clang.cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION
                        # Works unless different specializations have different APIs
                        ]:
                    pass
                else:
                    raise NotImplementedError("Unsupported public cursor kind: {} at {}".format(cursor.kind, cursor.location))
            else:
                if cursor.kind == clang.cindex.CursorKind.FIELD_DECL:
                    children.append(self.__convert_member(cursor))
                elif cursor.kind == clang.cindex.CursorKind.VAR_DECL:
                    children.append(self.__convert_variable(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
                    children.append(self.__convert_base(cursor))
                elif cursor.kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL]:
                    # We assume no forward declarations of private classes
                    children.append(self.__convert_class(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
                    children.append(self.__convert_template(cursor))
                elif cursor.kind in [
                        clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL,
                        clang.cindex.CursorKind.CXX_METHOD,
                        # Just ignore private constructors and destructors
                        clang.cindex.CursorKind.CONSTRUCTOR,
                        clang.cindex.CursorKind.DESTRUCTOR,
                        # Just ignore private enumerations
                        clang.cindex.CursorKind.ENUM_DECL,
                        # Just ignore private typedefs
                        clang.cindex.CursorKind.TYPEDEF_DECL,
                        clang.cindex.CursorKind.FUNCTION_TEMPLATE
                    ]:
                    pass
                else:
                    raise NotImplementedError("Unsupported private cursor kind: {} at {}".format(cursor.kind, cursor.location))
        return children

    def ToIR(self, project, with_include="", spec_include="", spec_private=""):
#        self.__print_tree(self.translation_unit.cursor, 0)
        self.project = project
        if self.translation_unit.cursor.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            raise InvalidNodeError
        namespace = IR.Namespace(
                name=project,
                children = self.__convert_children(self.translation_unit.cursor.get_children()),
                with_include = with_include,
                spec_include = spec_include,
                spec_private = spec_private
                )
        namespace.InstantiateTemplates()
        return namespace
