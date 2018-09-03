
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
                    return_type = IR.Type_Reference(name = IR.Identifier([cursor.result_type.spelling]))))
        return functions

    def __parse_arguments(self, cursors):
        argv = []
        argc = 1
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.PARM_DECL:
                ptype = IR.Type_Reference(name = IR.Identifier([cursor.type.spelling]))
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
                members.append(IR.Variable(name = cursor.displayname, ctype = IR.Type_Reference(name=IR.Identifier([cursor.type.spelling]))))
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

    def ToIR(self):
        #self.__print_tree(self.translation_unit.cursor, 0)
        if self.translation_unit.cursor.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            raise InvalidNodeError
        for cursor in self.translation_unit.cursor.get_children():
            if cursor.kind == clang.cindex.CursorKind.NAMESPACE:
                return self.__parse_namespace(cursor)
            elif cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
                return self.__parse_class(cursor)
