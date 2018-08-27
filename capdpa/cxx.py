
import clang.cindex
import IR

class InvalidNodeError: pass

class CXX:

    def __init__(self, header):
        self.index = clang.cindex.Index.create()
        self.translation_unit = self.index.parse(header, ["-x", "c++"])

    def __print_layer(self, cursor):
        print(str(cursor.kind) + " (" + cursor.displayname + "): " + str([cursor.kind for cursor in cursor.get_children()]))

    def __parse_class(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.CLASS_DECL:
            raise InvalidNodeError
        return IR.Class(
                name = IR.Identifier([cursor.displayname]))

    def __parse_constant(self, cursor):
        if cursor.kind != clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
            raise InvalidNodeError
        return IR.Constant(
                name = IR.Identifier([cursor.displayname]),
                value = cursor.enum_value)

    def __parse_named_enum(self, cursors):
        enums = []
        for cursor in cursors:
            if cursor.kind == clang.cindex.CursorKind.ENUM_DECL and cursor.displayname:
                enums.append(IR.Enum(
                    name = IR.Identifier([cursor.displayname]),
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
                name = IR.Identifier([cursor.displayname]),
                enums = self.__parse_named_enum(cursor.get_children()),
                constants = self.__parse_anonymous_enum(cursor.get_children())
                )

    def ToIR(self):
        if self.translation_unit.cursor.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            raise InvalidNodeError
        for cursor in self.translation_unit.cursor.get_children():
            if cursor.kind == clang.cindex.CursorKind.NAMESPACE:
                return self.__parse_namespace(cursor)
            elif cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
                return self.__parse_class(cursor)
