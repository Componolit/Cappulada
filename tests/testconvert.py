
import unittest
import clang.cindex
from capdpa import *
from capdpa_test import *

class Parser(Capdpa_Test):

    def test_empty_namespace(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "Empty")])
        result = CXX("tests/data/test_empty_namespace.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_constants(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "With_constants",
            children = [
                Constant(name = "X", value = 1),
                Constant(name = "Y", value = 2),
                Constant(name = "Z", value = 3)])])
        result = CXX("tests/data/test_namespace_with_constants.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_empty_class(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "Empty")])
        result = CXX("tests/data/test_empty_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_default_constructor(self):
        expected = Class(name="Test", children=[
            Constructor(symbol=""),
            Function(name="f1", symbol="")])
        result = Class(name="Test", children=[
            Function(name="f1", symbol="")])
        self.check(result, expected)

    def test_namespace_with_class(self):
        expected = Namespace(name = "Capdpa", children = [Namespace (name = "With_class",
                children = [Class(name = "In_namespace")])])
        result = CXX("tests/data/test_namespace_with_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_enum(self):
        expected = Namespace(name = "Capdpa", children = [Namespace (name = "With_enum",
                children = [
                    Enum(name = "WEEKEND", children = [
                        Constant(name = "SATURDAY", value = 0),
                        Constant(name = "SUNDAY", value = 1)]),
                    Enum(name = "Constants", children = [
                        Constant(name = "ONE", value = 1),
                        Constant(name = "TWO", value = 2),
                        Constant(name = "THREE", value = 3)])])])
        result = CXX("tests/data/test_namespace_with_enum.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_constants(self):
        expected = Namespace(name = "Capdpa", children = [Class (name = "With_constants",
                children = [Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Constant(name = "THREE", value = 3),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_ONE", value = -1),
                        Constant(name = "MINUS_TWO", value = -2),
                        Constant(name = "MINUS_THREE", value = -3)])])])
        result = CXX("tests/data/test_class_with_constants.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_members(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "With_members",
                children = [
                    Variable (name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                    Variable (name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"]), pointer = 0)),
                    Variable (name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                    Variable (name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                    Variable (name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"])), access="private"),
                    Variable (name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
                    ])])
        result = CXX("tests/data/test_class_with_members.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_functions(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "With_functions",
                children = [
                    Function(name = "public_function", symbol = "", parameters = [
                        Variable (name = "arg1", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))]),
                    Function(name = "named_param", symbol = "", parameters = [
                        Variable (name = "param", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))],
                        return_type = Type_Reference(name = Identifier(["Capdpa", "int"]))
                        ),
                    Constructor(symbol = "")])])
        result = CXX("tests/data/test_class_with_functions.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_class_with_everything(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "With_class", children = [
            Class(name = "With_everything",
                children = [
                    Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_ONE", value = -1),
                        Constant(name = "MINUS_TWO", value = -2)]),
                    Variable(name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                    Function(name = "public_function", symbol = ""),
                    Variable(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                    Constructor(symbol = "")])])])
        result = CXX("tests/data/test_namespace_with_class_with_everything.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_class_type(self):
        expected = Namespace(name = "Capdpa", children = [
                Namespace (name = "With_class",
                    children = [Class(name = "In_namespace")]),
                Class(name = "Full",
                    children = [
                        Variable(name = "value", ctype = Type_Reference(name = Identifier(["Capdpa", "With_class", "In_namespace", "Class"]))),
                        Variable(name = "value_ptr", ctype = Type_Reference(name = Identifier(["Capdpa", "With_class", "In_namespace", "Class"]), pointer = 1))
                    ])])
        result = CXX("tests/data/test_class_with_class_type.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_types(self):
        expected = Namespace(name = "Capdpa", children = [
                Type_Definition(
                    name="uint8_t",
                    reference=Type_Reference(name=Identifier(name=["Capdpa", "unsigned_char"]), pointer=0)),
                Type_Definition(
                    name="int32_t",
                    reference=Type_Reference(name=Identifier(name=["Capdpa", "int"]), pointer=0)),
                Type_Definition(name="u8", reference=Type_Reference(name=Identifier(name=["uint8_t"]), pointer=0)),
                Type_Definition(name="ull", reference=Type_Reference(name=Identifier(name=["Capdpa", "unsigned_long_long"])))])
        result = CXX("tests/data/test_types.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_template_conversion(self):
        cxx = CXX("tests/data/test_with_template.h")
        cursor = list(cxx.translation_unit.cursor.get_children())[0]
        template = getattr(CXX, "_CXX__convert_template")(cxx, cursor)
        expected = Template(entity=Class(name="Container", children=[
            Variable(name="a", ctype=Template_Argument(name="A")),
            Variable(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")])

    def test_template_engine(self):
        types = Type_Reference_Template(name="Container", arguments=[
            Type_Reference(name=Identifier(["typeA"])),
            Type_Reference(name=Identifier(["typeB"]))])
        expected = Class(name="Container_T_typeA_typeB", children=[
            Variable(name="a", ctype=Type_Reference(name=Identifier(["typeA"]))),
            Variable(name="b", ctype=Type_Reference(name=Identifier(["typeB"])))])
        template = Template(entity=Class(name="Container", children=[
            Variable(name="a", ctype=Template_Argument(name="A")),
            Variable(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")])
        result = template.instantiate(types)
        self.check(result, expected)
        self.check(template, Template(entity=Class(name="Container", children=[
            Variable(name="a", ctype=Template_Argument(name="A")),
            Variable(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")]))

    def test_template(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=Class(name="Container", children=[
                Variable(name="a", ctype=Template_Argument(name="A")),
                Variable(name="b", ctype=Template_Argument(name="B")),
                Constructor(symbol="", parameters=[])]), typenames=[
                    Template_Argument(name="A"),
                    Template_Argument(name="B")]),
            Class(name = "Container_T_int_signed_char", children = [
                Variable(name = "a", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Variable(name = "b", ctype = Type_Reference(name = Identifier(["Capdpa", "signed_char"])))]),
            Class(name = "Container_T_int_int", children = [
                Variable(name = "a", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Variable(name = "b", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))]),
            Class(name = "User", children = [
                Variable(name = "cic", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Container"]), arguments = [
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "signed_char"]))])),
                Variable(name = "cii", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Container"]), arguments = [
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "int"]))])),
                Variable(name = "cic2", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Container"]), arguments = [
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "signed_char"]))]))
                ])])
        result = CXX("tests/data/test_with_template.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_inheritance_simple(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_members", children = [
                Variable (name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Variable (name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"]), pointer = 0)),
                Variable (name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                Variable (name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                Variable (name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"])), access="private"),
                Variable (name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
            ]),
            Class(name = "Inheritance", children = [
                Class_Reference(name = Identifier(["Capdpa", "With_members"])),
                Variable (name = "Additional", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))
            ])])
        result = CXX("tests/data/test_class_inheritance.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_inheritance_chain(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_members", children = [
                Variable (name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Variable (name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"]), pointer = 0)),
                Variable (name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                Variable (name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                Variable (name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"])), access="private"),
                Variable (name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
            ]),
            Class(name = "Inheritance", children = [
                Class_Reference(name = Identifier(["Capdpa", "With_members"])),
                Variable (name = "Additional", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))
            ]),
            Class(name = "Child", children = [
                Class_Reference(name = Identifier(["Capdpa", "Inheritance"])),
                Variable (name = "c", ctype = Type_Reference(name = Identifier(["Capdpa", "long"])))
            ])])
        result = CXX("tests/data/test_class_inheritance_child.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_virtual(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Virtual", children = [
                    Function(name = "foo", symbol = "", return_type = None, virtual = True)
                ])])
        result = CXX("tests/data/test_base_with_virtual.h").ToIR(project="Capdpa")
        self.check(result, expected)
        self.check(result["With_Virtual"].isVirtual(), True)

    def test_inherit_from_virtual(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Virtual", children = [
                Function(name = "foo", symbol = "", return_type = None, virtual = True)
            ]),
            Class(name = "From_Virtual",
                children = [
                    Class_Reference(name = Identifier(["Capdpa", "With_Virtual"])),
                    Variable(name = "v", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))])])
        result = CXX("tests/data/test_inherit_from_virtual.h").ToIR(project="Capdpa")
        self.check(result, expected)
        self.check(result["From_Virtual"].isVirtual(), True)

    def test_inherit_virtual_from_simple(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_members", children = [
                Variable (name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Variable (name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"]), pointer = 0)),
                Variable (name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                Variable (name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                Variable (name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "C_Address"])), access="private"),
                Variable (name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
            ]),
            Class(name = "Inheritance", children = [
                Class_Reference(name = Identifier(["Capdpa", "With_members"])),
                Variable (name = "Additional", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))
            ]),
            Class(name = "Simple", children = [
                Class_Reference(name = Identifier(["Capdpa", "Inheritance"])),
                Variable(name = "s", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Function(name = "foo", symbol = "", virtual=True)])])
        result = CXX("tests/data/test_inherit_virtual_from_simple.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_empty_struct(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "S")])
        result = CXX("tests/data/test_empty_struct.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_without_access_spec(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "No_access", children = [
                Variable(name="x", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private")])])
        result = CXX("tests/data/test_class_without_access_spec.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_struct_without_access_spec(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "No_access", children = [
                Variable(name="x", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="public")])])
        result = CXX("tests/data/test_struct_without_access_spec.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_nested_class(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "Outer", children = [
                Class(name = "Inner"),
                Variable(name = "i", ctype = Type_Reference(name = Identifier(["Capdpa", "Outer", "Inner", "Class"])))])])
        result = CXX("tests/data/test_nested_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_pointer_member(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Pointer", children = [
                Variable(name="p", ctype=Type_Reference(name = Identifier(["Capdpa", "int"]), pointer = 1))])
            ])
        result = CXX("tests/data/test_pointer_member.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_reference_member(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Reference", children = [
                Variable(name="r", ctype=Type_Reference(name=Identifier(["Capdpa", "int"]), reference=True))])])
        result = CXX("tests/data/test_reference_member.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_enum_member(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Enum", children = [
                Enum(name = "E_t", children = [
                    Constant(name = "A", value = 0),
                    Constant(name = "B", value = 1)]),
                Variable(name = "E", ctype=Type_Reference(name = Identifier(["Capdpa", "With_Enum", "E_t"])))])])
        result = CXX("tests/data/test_enum_member.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_array(self):
        CXX("tests/data/test_class_with_array.h").ToIR(project="Capdpa")

    def test_array_template(self):
        CXX("tests/data/test_array_template.h").ToIR(project="Capdpa")

    def test_template_typedef(self):
        CXX("tests/data/test_template_typedef.h").ToIR(project="Capdpa")

    def test_class_with_struct_type(self):
        expected = Namespace("Capdpa", children = [
            Class(name = "With_Struct", children = [
                Class(name = "Ws"),
                Variable(name = "value", ctype = Type_Reference(name = Identifier(["Capdpa", "With_Struct", "Ws", "Class"])))])])
        result = CXX("tests/data/test_class_with_struct_type.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_template(self):
        expected = Namespace("Capdpa", children = [
            Class(name = "Template", children = [
                Constructor(parameters = [
                    Variable(name = "other", ctype =
                        Type_Reference(name = Identifier(["Capdpa", "Template"]), reference=True))],
                    symbol = "")])])
        result = CXX("tests/data/test_class_template.h").ToIR(project="Capdpa")
        self.check(result, expected)
