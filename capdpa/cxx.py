
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
        clang.cindex.TypeKind.BOOL      : "boolean",
        clang.cindex.TypeKind.CHAR_U    : "unsigned_char",
        clang.cindex.TypeKind.UCHAR     : "unsigned_char",
        clang.cindex.TypeKind.USHORT    : "unsigned_short",
        clang.cindex.TypeKind.UINT      : "unsigned_int",
        clang.cindex.TypeKind.ULONG     : "unsigned_long",
        clang.cindex.TypeKind.ULONGLONG : "unsigned_long_long",
        clang.cindex.TypeKind.CHAR_S    : "signed_char",
        clang.cindex.TypeKind.SCHAR     : "signed_char",
        clang.cindex.TypeKind.WCHAR     : "wide_char",
        clang.cindex.TypeKind.SHORT     : "short",
        clang.cindex.TypeKind.INT       : "int",
        clang.cindex.TypeKind.LONG      : "long",
        clang.cindex.TypeKind.LONGLONG  : "long_long",
        clang.cindex.TypeKind.FLOAT     : "C_float",
        clang.cindex.TypeKind.DOUBLE    : "double",
        clang.cindex.TypeKind.LONGDOUBLE: "long_double"
        }

class CXX:

    def __init__(self, header, flags = []):
        self.index = clang.cindex.Index.create()
        self.translation_unit = self.index.parse(header, ["-x", "c++"] + flags)

    def __print_layer(self, cursor):
        print(str(cursor.kind) + " (" + cursor.displayname + "): " + str([cursor.kind for cursor in cursor.get_children()]))

    def __print_tree(self, cursor, indent):
        print(" " * indent + (cursor.displayname or "UNNAMED") + " (" + str(cursor.kind) + ")")
        for c in cursor.get_children():
            self.__print_tree(c, indent + 2)

    def __convert_class(self, cursor):
        if cursor.kind not in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL]:
            raise InvalidNodeError
        return IR.Class(
                name = cursor.displayname,
                children = self.__convert_children(cursor.get_children()))

    def __convert_base(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            raise InvalidNodeError
        return IR.Class_Reference(name=
                IR.Identifier(self.__resolve_name(cursor.type.get_declaration())))

    def __convert_function(self, cursor):
        return IR.Function(
                name = cursor.spelling,
                symbol = "",
                parameters = self.__convert_arguments(cursor.get_children()),
                return_type = self.__convert_type([], cursor.result_type),
                virtual = cursor.is_virtual_method())

    def __convert_constructor(self, cursor):
        return IR.Constructor(
                symbol = "",
                parameters = self.__convert_arguments(cursor.get_children()))

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

        const = type_cursor.is_const_qualified()

        if type_cursor.kind == clang.cindex.TypeKind.LVALUEREFERENCE:
            reference = True
            type_cursor = type_cursor.get_pointee()
        if type_cursor.kind in [clang.cindex.TypeKind.UNEXPOSED, clang.cindex.TypeKind.RECORD]:
            targs = type_cursor.get_num_template_arguments()
            decl = type_cursor.get_declaration()
            if targs > 0:
                if children and children[0].kind == clang.cindex.CursorKind.TEMPLATE_REF:
                    literals = children[1:]
                args = []
                for i in range(targs):
                    if type_cursor.get_template_argument_type(i).kind != clang.cindex.TypeKind.INVALID:
                        args.append(self.__convert_type(children, type_cursor.get_template_argument_type(i)))
                    else:
                        args.append(IR.Type_Literal(value = eval(list(literals[0].get_tokens())[0].spelling)))
                        literals = literals[1:]
                return IR.Type_Reference_Template(
                        name = IR.Identifier(self.__resolve_name(decl)),
                        constant = const,
                        arguments = args,
                        pointer = ptr, reference=reference)
            elif decl.kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL]:
                return IR.Type_Reference(
                        name = IR.Identifier(self.__resolve_name(decl) + ["Class"]),
                        constant = const,
                        pointer = ptr, reference=reference)
            elif decl.kind in [clang.cindex.CursorKind.ENUM_DECL, clang.cindex.CursorKind.TYPEDEF_DECL]:
                return IR.Type_Reference(
                        name = IR.Identifier(self.__resolve_name(decl)),
                        pointer = ptr,
                        reference = reference)
            elif decl.kind == clang.cindex.CursorKind.NO_DECL_FOUND:
                canon = type_cursor.get_canonical().kind
                if canon == clang.cindex.TypeKind.UNEXPOSED:
                    return IR.Template_Argument(type_cursor.spelling)
                elif canon == clang.cindex.TypeKind.FUNCTIONPROTO:
                    return IR.Function_Reference()
                else:
                    raise NotImplementedError("Unknown undeclared canonical type: {}".format(canon))
            else:
                raise NotImplementedError("Unsupported declaration kind {} at {}".format(decl.kind, decl.location))
        elif type_cursor.kind ==  clang.cindex.TypeKind.VOID:
            return IR.Type_Reference(
                name = IR.Identifier([self.project, "C_Address"]),
                constant = const,
                pointer = ptr - 1,
                reference = reference) if ptr else None
        elif type_cursor.kind ==  clang.cindex.TypeKind.TYPEDEF:
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
                return IR.Function_Reference(parameters = [
                    IR.Variable(
                        name="This",
                        ctype=IR.Type_Reference(name=IR.Identifier(
                            self.__resolve_name(type_cursor.get_class_type().get_declaration())),
                            constant = False,
                            reference=True))])
                        #FIXME: all parameters
            elif parent_type == clang.cindex.TypeKind.UNEXPOSED:
                return IR.Function_Reference(parameters = [
                    IR.Variable(
                        name="This",
                        ctype=IR.Template_Argument(type_cursor.get_class_type().spelling))])
            else:
                raise NotImplementedError("Unsupported type of memberpointer: {}".format(parent_type))
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
                    argv.append(IR.Variable(name = cursor.displayname, ctype = ptype))
                else:
                    argv.append(IR.Variable(name = "arg" + str(argc), ctype = ptype))
                argc += 1
        return argv

    def __convert_member(self, cursor):
        return IR.Variable(
                name = cursor.displayname,
                ctype = self.__convert_type(list(cursor.get_children()), cursor.type),
                access="public" if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC else "private")

    def __convert_constant(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
            raise InvalidNodeError
        return IR.Constant(
                name = cursor.displayname,
                value = cursor.enum_value)

    def __convert_enum(self, cursor):
        return IR.Enum(
                    name = cursor.displayname,
                    children = [self.__convert_constant(constant) for constant in cursor.get_children()])

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
            resolved = self.__convert_type([], children[0].type)
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
                    children = self.__convert_children(list(cursor.get_children())[len(targs):])),
                typenames = [IR.Template_Argument(c.spelling) for c in targs])


    def __convert_children(self, cursors):
        children = []
        clist = list(cursors)
        for cursor in clist:
            if cursor.access_specifier in [clang.cindex.AccessSpecifier.PUBLIC, clang.cindex.AccessSpecifier.INVALID]:
                if cursor.kind == clang.cindex.CursorKind.NAMESPACE:
                    children.append(self.__convert_namespace(cursor))
                elif cursor.kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL]:
                    decl = self.__convert_class(cursor)
                    if True not in [c.name == decl.name for c in children]:
                        if not cursor.is_definition():
                            if cursor.get_definition() and cursor.get_definition() in clist:
                                children.append(self.__convert_class(cursor.get_definition()))
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
                    children.append(self.__convert_function(cursor))
                elif cursor.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
                    children.append(self.__convert_typedef(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CONSTRUCTOR:
                    children.append(self.__convert_constructor(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
                    children.append(self.__convert_template(cursor))
                elif cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
                    children.append(self.__convert_base(cursor))
                elif cursor.kind == clang.cindex.CursorKind.FIELD_DECL:
                    children.append(self.__convert_member(cursor))
                elif cursor.kind in [clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL, clang.cindex.CursorKind.UNEXPOSED_DECL]:
                    pass
                else:
                    raise NotImplementedError("Unsupported cursor kind: {} at {}".format(cursor.kind, cursor.location))
            else:
                if cursor.kind == clang.cindex.CursorKind.FIELD_DECL:
                    children.append(self.__convert_member(cursor))
        return children

    def ToIR(self, project):
#        self.__print_tree(self.translation_unit.cursor, 0)
        self.project = project
        if self.translation_unit.cursor.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            raise InvalidNodeError
        namespace = IR.Namespace(
                name=project,
                children = self.__convert_children(self.translation_unit.cursor.get_children())
                )
        namespace.InstantiateTemplates()
        return namespace
