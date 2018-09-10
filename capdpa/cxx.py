
import clang.cindex
import IR

class InvalidNodeError: pass

class CXX:

    def __init__(self, header):
        self.index = clang.cindex.Index.create()
        self.translation_unit = self.index.parse(header, ["-x", "c++"])

    def __print_layer(self, cursor):
        print(str(cursor.kind) + " (" + cursor.displayname + "): " + str([cursor.kind for cursor in cursor.get_children()]))

    def __print_tree(self, cursor, indent):
        print(" " * indent + (cursor.displayname or "UNNAMED") + " (" + str(cursor.kind) + ")")
        for c in cursor.get_children():
            self.__print_tree(c, indent + 2)

    def __parse_class(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.CLASS_DECL:
            raise InvalidNodeError
        return IR.Class(
                name = cursor.displayname,
                enums = self.__parse_named_enum(cursor.get_children()),
                constants = self.__parse_anonymous_enum(cursor.get_children()),
                members = self.__parse_members(cursor.get_children()),
                functions = self.__parse_functions(cursor.get_children())
                )

    def __parse_functions(self, cursors):
        public = True
        functions = []
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL:
                public = list(cursor.get_tokens())[0].spelling == "public"
            if cursor.kind == clang.cindex.CursorKind.CXX_METHOD and public:
                functions.append(IR.Function(
                    name = cursor.spelling,
                    symbol = "",
                    parameters = self.__parse_arguments(cursor.get_children()),
                    return_type = self.__parse_type(cursor.result_type)))
        return functions

    def __resolve_name(self, cursor):
        identifier = []
        while cursor.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            identifier.append(cursor.spelling)
            cursor = cursor.semantic_parent
        return list(reversed(identifier))

    def __parse_type(self, type_cursor):
        ptr = 0;
        while type_cursor.kind == clang.cindex.TypeKind.POINTER:
            ptr += 1
            type_cursor = type_cursor.get_pointee()
        try:
            return {
                    clang.cindex.TypeKind.UNEXPOSED:
                        lambda: IR.Type_Reference(name = IR.Identifier(self.__resolve_name(type_cursor.get_declaration())), pointer = ptr, builtin=False),
                    clang.cindex.TypeKind.VOID:
                        lambda: IR.Type_Reference(name = IR.Identifier(["void"]), pointer = ptr),
                    clang.cindex.TypeKind.BOOL:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Boolean"]), pointer = ptr),
                    clang.cindex.TypeKind.UCHAR:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "unsigned_char"]), pointer = ptr),
                    clang.cindex.TypeKind.USHORT:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "unsigned_short"]), pointer = ptr),
                    clang.cindex.TypeKind.UINT:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "unsigned_int"]), pointer = ptr),
                    clang.cindex.TypeKind.ULONG:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "unsigned_long"]), pointer = ptr),
                    clang.cindex.TypeKind.SCHAR:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "signed_char"]), pointer = ptr),
                    clang.cindex.TypeKind.WCHAR:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "wchar_t"]), pointer = ptr),
                    clang.cindex.TypeKind.SHORT:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "short"]), pointer = ptr),
                    clang.cindex.TypeKind.INT:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "int"]), pointer = ptr),
                    clang.cindex.TypeKind.LONG:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "long"]), pointer = ptr),
                    clang.cindex.TypeKind.LONGLONG:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "long_long"]), pointer = ptr),
                    clang.cindex.TypeKind.FLOAT:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "C_float"]), pointer = ptr),
                    clang.cindex.TypeKind.DOUBLE:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "double"]), pointer = ptr),
                    clang.cindex.TypeKind.LONGDOUBLE:
                        lambda: IR.Type_Reference(name = IR.Identifier(["Capdpa", "Types", "long_double"]), pointer = ptr),
                    clang.cindex.TypeKind.TYPEDEF:
                        lambda: IR.Type_Reference(name = IR.Identifier([type_cursor.spelling]), pointer = ptr, builtin = False)
                    }[type_cursor.kind]()
        except KeyError:
            raise NotImplementedError("Unsupported type: {} (from {})".format(str(type_cursor.kind), type_cursor.spelling))

    def __parse_arguments(self, cursors):
        argv = []
        argc = 1
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.PARM_DECL:
                ptype = self.__parse_type(cursor.type)
                if cursor.displayname:
                    argv.append(IR.Variable(name = cursor.displayname, ctype = ptype))
                else:
                    argv.append(IR.Variable(name = "arg" + str(argc), ctype = ptype))
                argc += 1
        return argv

    def __parse_members(self, cursors):
        public = True
        members = []
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL:
                public = list(cursor.get_tokens())[0].spelling == "public"
            if cursor.kind == clang.cindex.CursorKind.FIELD_DECL and public:
                members.append(IR.Variable(name = cursor.displayname, ctype = self.__parse_type(cursor.type)))
        return members

    def __parse_constant(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
            raise InvalidNodeError
        return IR.Constant(
                name = cursor.displayname,
                value = cursor.enum_value)

    def __parse_named_enum(self, cursors):
        enums = []
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.ENUM_DECL and cursor.displayname:
                enums.append(IR.Enum(
                    name = cursor.displayname,
                    constants = [self.__parse_constant(constant) for constant in cursor.get_children()]))
        return enums

    def __parse_anonymous_enum(self, cursors):
        constants = []
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.ENUM_DECL and not cursor.displayname:
                constants.extend([self.__parse_constant(constant) for constant in cursor.get_children()])
        return constants

    def __parse_namespace(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.NAMESPACE:
            raise InvalidNodeError
        return IR.Namespace(
                name = cursor.displayname,
                enums = self.__parse_named_enum(cursor.get_children()),
                constants = self.__parse_anonymous_enum(cursor.get_children()),
                classes = [self.__parse_class(c) for c in cursor.get_children() if c.kind == clang.cindex.CursorKind.CLASS_DECL]
                )

    def __parse_typedef(self, cursor):
        children = list(cursor.get_children())
        if children:
            resolved = self.__parse_type(children[0].type)
        else:
            resolved = self.__parse_type(cursor.type.get_canonical())
        return IR.Type_Definition(cursor.type.spelling, resolved)

    def __parse_tree(self, cursor):
        if cursor.kind == clang.cindex.CursorKind.NAMESPACE:
            return self.__parse_namespace(cursor)
        elif cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
            return self.__parse_class(cursor)
        elif cursor.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
            return self.__parse_typedef(cursor);
        else:
            raise NotImplementedError ("Top level node {} is not implemented".format(cursor.kind))

    def ToIR(self):
#        self.__print_tree(self.translation_unit.cursor, 0)
        if self.translation_unit.cursor.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            raise InvalidNodeError
        return [self.__parse_tree(cursor) for cursor in self.translation_unit.cursor.get_children()]
