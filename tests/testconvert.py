#!/usr/bin/env python

import sys
if __name__ == '__main__':
    sys.path.append (".")

import unittest
import clang.cindex
from capdpa import *
from capdpa_test import *

class Parser(Capdpa_Test):

    def test_empty_namespace(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "Empty")])
        result = CXX("tests/data/convert/test_empty_namespace.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_constants(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "With_constants",
            children = [
                Constant(name = "X", value = 1),
                Constant(name = "Y", value = 2),
                Constant(name = "Z", value = 3)])])
        result = CXX("tests/data/convert/test_namespace_with_constants.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_empty_class(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "Empty")])
        result = CXX("tests/data/convert/test_empty_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_default_constructor(self):
        expected = Class(name="Test", children=[
            Constructor(),
            Method(name="f1")])
        result = Class(name="Test", children=[
            Method(name="f1")])
        self.check(result, expected)

    def test_namespace_with_class(self):
        expected = Namespace(name = "Capdpa", children = [Namespace (name = "With_class",
                children = [Class(name = "In_namespace")])])
        result = CXX("tests/data/convert/test_namespace_with_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_enum(self):
        expected = Namespace(name = "Capdpa", children = [Namespace (name = "With_enum",
                children = [
                    Enum(name = "WEEKEND", children = [
                        Constant(name = "SATURDAY", value = 0),
                        Constant(name = "SUNDAY", value = 1)],
                        ctype = Type_Reference(name = Identifier(["Capdpa", "unsigned_int"]))),
                    Enum(name = "Constants", children = [
                        Constant(name = "ONE", value = 1),
                        Constant(name = "TWO", value = 2),
                        Constant(name = "THREE", value = 3)],
                        ctype = Type_Reference(name = Identifier(["Capdpa", "unsigned_int"])))])])
        result = CXX("tests/data/convert/test_namespace_with_enum.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_constants(self):
        expected = Namespace(name = "Capdpa", children = [Class (name = "With_constants",
                children = [Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Constant(name = "THREE", value = 3),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_THREE", value = -3),
                        Constant(name = "MINUS_TWO", value = -2),
                        Constant(name = "MINUS_ONE", value = -1)],
                        ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))])])
        result = CXX("tests/data/convert/test_class_with_constants.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_members(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "With_members",
                children = [
                    Member(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                    Member(name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1)),
                    Member(name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                    Member(name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                    Member(name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1), access="private"),
                    Member(name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
                    ])])
        result = CXX("tests/data/convert/test_class_with_members.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_functions(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "With_functions",
                children = [
                    Method(name = "public_function", parameters = [
                        Argument(name = "arg1", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))]),
                    Method(name = "named_param", parameters = [
                        Argument(name = "param", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))],
                        return_type = Type_Reference(name = Identifier(["Capdpa", "int"]))
                        ),
                    Constructor()])])
        result = CXX("tests/data/convert/test_class_with_functions.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_class_with_everything(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "With_class", children = [
            Class(name = "With_everything",
                children = [
                    Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_TWO", value = -2),
                        Constant(name = "MINUS_ONE", value = -1)],
                        ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                    Member(name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                    Method(name = "public_function"),
                    Member(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                    Constructor()])])])
        result = CXX("tests/data/convert/test_namespace_with_class_with_everything.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_class_type(self):
        expected = Namespace(name = "Capdpa", children = [
                Namespace (name = "With_class",
                    children = [Class(name = "In_namespace")]),
                Class(name = "Full",
                    children = [
                        Member(name = "value", ctype = Type_Reference(name = Identifier(["Capdpa", "With_class", "In_namespace", "Class"]))),
                        Member(name = "value_ptr", ctype = Type_Reference(name = Identifier(["Capdpa", "With_class", "In_namespace", "Class"]), pointer = 1))
                    ])])
        result = CXX("tests/data/convert/test_class_with_class_type.h").ToIR(project="Capdpa")
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
                Type_Definition(name="ull", reference=Type_Reference(name=Identifier(name=["Capdpa", "unsigned_long_long"]))),
                Type_Definition(name="int8_t", reference=Type_Reference(name=Identifier(["Capdpa", "char"]))),
                Type_Definition(name="int16_t", reference=Type_Reference(name=Identifier(["Capdpa", "short"])))])
        result = CXX("tests/data/convert/test_types.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_template_conversion(self):
        cxx = CXX("tests/data/convert/test_with_template.h")
        cursor = list(cxx.translation_unit.cursor.get_children())[0]
        template = getattr(CXX, "_CXX__convert_template")(cxx, cursor)
        expected = Template(entity=Class(name="Container", children=[
            Member(name="a", ctype=Template_Argument(name="A")),
            Member(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")])

    def test_template_engine(self):
        types = Type_Reference_Template(name="Container", arguments=[
            Type_Reference(name=Identifier(["typeA"])),
            Type_Reference(name=Identifier(["typeB"]))])
        expected = Class(name="Container_T_Typea_Typeb", children=[
            Member(name="a", ctype=Type_Reference(name=Identifier(["typeA"]))),
            Member(name="b", ctype=Type_Reference(name=Identifier(["typeB"])))],
            instanceof = (['Container'], [Type_Reference(constant=False,name=Identifier(name=['typeA']),pointer=0,reference=False),
                                          Type_Reference(constant=False,name=Identifier(name=['typeB']),pointer=0,reference=False)]))
        template = Template(entity=Class(name="Container", children=[
            Member(name="a", ctype=Template_Argument(name="A")),
            Member(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")])
        result = template.instantiate(types)
        self.check(result, expected)
        self.check(template, Template(entity=Class(name="Container", children=[
            Member(name="a", ctype=Template_Argument(name="A")),
            Member(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")]))
        ftypes = Type_Reference_Template(name = "Base", arguments = [
            Type_Reference(name = Identifier(["Capdpa", "ClassA"]))])
        ftemplate = Template(entity=Class(name = "F", children=[
            Method(name = "Foo", parameters = [
                Argument(name = "x", ctype = Template_Argument(name="T"))],
                return_type=Template_Argument(name="T")),
            Member(name = "Bar", ctype=Function_Reference(parameters = [
                Argument(name = "x", ctype = Template_Argument(name="T"))],
                return_type=Template_Argument(name="T")))
            ]),
            typenames = [
                Template_Argument(name = "T")])
        fexpected = Class(name="F_T_Classa", children = [
            Method(name = "Foo", parameters = [
                Argument(name = "x", ctype = Type_Reference(name = Identifier(["Capdpa", "ClassA"])))],
                return_type = Type_Reference(name = Identifier(["Capdpa", "ClassA"]))),
            Member(name = "Bar", ctype = Function_Reference(parameters = [
                Argument(name = "x", ctype = Type_Reference(name = Identifier(["Capdpa", "ClassA"])))],
                return_type = Type_Reference(name = Identifier(["Capdpa", "ClassA"]))))
            ],
            instanceof = (['F'], [Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'ClassA']),pointer=0,reference=False)]))
        self.check(ftemplate.instantiate(ftypes), fexpected)

    def test_template(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=Class(name="Container", children=[
                Member(name="a", ctype=Template_Argument(name="A")),
                Member(name="b", ctype=Template_Argument(name="B")),
                Constructor(parameters=[])]), typenames=[
                    Template_Argument(name="A"),
                    Template_Argument(name="B")]),
            Class(name = "Container_T_Int_Char", children = [
                Member(name = "a", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Member(name = "b", ctype = Type_Reference(name = Identifier(["Capdpa", "char"])))],
                instanceof=(['Capdpa', 'Container'], [Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'int']),pointer=0,reference=False),
                                                      Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'char']),pointer=0,reference=False)])),
            Class(name = "Container_T_Int_Int", children = [
                Member(name = "a", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Member(name = "b", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))],
                instanceof=(['Capdpa', 'Container'], [Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'int']),pointer=0,reference=False),
                                                      Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'int']),pointer=0,reference=False)])),
            Class(name = "User", children = [
                Member(name = "cic", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Container"]), arguments = [
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "char"]))])),
                Member(name = "cii", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Container"]), arguments = [
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "int"]))])),
                Member(name = "cic2", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Container"]), arguments = [
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "char"]))]))
                ])])
        result = CXX("tests/data/convert/test_with_template.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_inheritance_simple(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_members", children = [
                Member(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Member(name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1)),
                Member(name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                Member(name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                Member(name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1), access="private"),
                Member(name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
            ]),
            Class(name = "Inheritance", children = [
                Class_Reference(name = Identifier(["Capdpa", "With_members"])),
                Member(name = "Additional", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))
            ])])
        result = CXX("tests/data/convert/test_class_inheritance.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_inheritance_chain(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_members", children = [
                Member(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Member(name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1)),
                Member(name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                Member(name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                Member(name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1), access="private"),
                Member(name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
            ]),
            Class(name = "Inheritance", children = [
                Class_Reference(name = Identifier(["Capdpa", "With_members"])),
                Member(name = "Additional", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))
            ]),
            Class(name = "Child", children = [
                Class_Reference(name = Identifier(["Capdpa", "Inheritance"])),
                Member(name = "c", ctype = Type_Reference(name = Identifier(["Capdpa", "long"])))
            ])])
        result = CXX("tests/data/convert/test_class_inheritance_child.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_virtual(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Virtual", children = [
                    Method(name = "foo", return_type = None, virtual = True)
                ])])
        result = CXX("tests/data/convert/test_base_with_virtual.h").ToIR(project="Capdpa")
        self.check(result, expected)
        self.check(result["With_Virtual"].isVirtual(), True)

    def test_inherit_from_virtual(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Virtual", children = [
                Method(name = "foo", return_type = None, virtual = True)
            ]),
            Class(name = "From_Virtual",
                children = [
                    Class_Reference(name = Identifier(["Capdpa", "With_Virtual"])),
                    Member(name = "v", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))])])
        result = CXX("tests/data/convert/test_inherit_from_virtual.h").ToIR(project="Capdpa")
        self.check(result, expected)
        self.check(result["From_Virtual"].isVirtual(), True)

    def test_inherit_virtual_from_simple(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_members", children = [
                Member(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Member(name = "public_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1)),
                Member(name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"]))),
                Member(name = "private_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private"),
                Member(name = "private_pointer", ctype = Type_Reference(name = Identifier(["Capdpa", "void"]), pointer = 1), access="private"),
                Member(name = "private_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])), access="private")
            ]),
            Class(name = "Inheritance", children = [
                Class_Reference(name = Identifier(["Capdpa", "With_members"])),
                Member(name = "Additional", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))
            ]),
            Class(name = "Simple", children = [
                Class_Reference(name = Identifier(["Capdpa", "Inheritance"])),
                Member(name = "s", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                Method(name = "foo", virtual=True)])])
        result = CXX("tests/data/convert/test_inherit_virtual_from_simple.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_empty_struct(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "S")])
        result = CXX("tests/data/convert/test_empty_struct.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_without_access_spec(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "No_access", children = [
                Member(name="x", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="private")])])
        result = CXX("tests/data/convert/test_class_without_access_spec.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_struct_without_access_spec(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "No_access", children = [
                Member(name="x", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])), access="public")])])
        result = CXX("tests/data/convert/test_struct_without_access_spec.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_nested_class(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "Outer", children = [
                Class(name = "Inner"),
                Member(name = "i", ctype = Type_Reference(name = Identifier(["Capdpa", "Outer", "Inner", "Class"])))])])
        result = CXX("tests/data/convert/test_nested_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_pointer_member(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Pointer", children = [
                Member(name="p", ctype=Type_Reference(name = Identifier(["Capdpa", "int"]), pointer = 1))])
            ])
        result = CXX("tests/data/convert/test_pointer_member.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_reference_member(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Reference", children = [
                Member(name="r", ctype=Type_Reference(name=Identifier(["Capdpa", "int"]), reference=True))])])
        result = CXX("tests/data/convert/test_reference_member.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_enum_member(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Enum", children = [
                Enum(name = "E_t", children = [
                    Constant(name = "A", value = 0),
                    Constant(name = "B", value = 1)],
                        ctype = Type_Reference(name = Identifier(["Capdpa", "unsigned_int"]))),
                Member(name = "e", ctype=Type_Reference(name = Identifier(["Capdpa", "With_Enum", "E_t"])))])])
        result = CXX("tests/data/convert/test_enum_member.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_array(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Array", children = [
                Member(name = "car", ctype = Array(
                    ctype = Type_Reference(name = Identifier(["Capdpa", "int"])),
                    size = 5))])])
        result = CXX("tests/data/convert/test_class_with_array.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_array_template(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=
                Class(name = "Template_With_Array", children = [
                    Member(name = "var", ctype = Array(
                        ctype = Type_Reference(name = Identifier(["Capdpa", "int"])),
                        size = Template_Argument(name = "Size")))]),
                    typenames = [Template_Argument(name = "Size")]
                    ),
            Class(name = "Template_With_Array_T_Int_5", children = [
                Member(name = "var", ctype = Array(
                    ctype = Type_Reference(name = Identifier(["Capdpa", "int"])),
                    size = 5))],
                instanceof = (["Capdpa", "Template_With_Array"], [Type_Literal(name=Identifier(["Capdpa", "int"]), value=5)])),
            Class(name = "With_Array_5", children = [
                Member(name = "twa", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Template_With_Array"]), arguments = [
                    Type_Literal(name = Identifier(["Capdpa", "int"]), value = 5)]))])])
        result = CXX("tests/data/convert/test_array_template.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_array_template_2(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=
                Class(name = "Cls", children = [
                    Member(name = "ar", ctype = Array(
                        ctype = Type_Reference(name = Identifier(["Capdpa", "int"])),
                        size = Template_Argument(name = "S")))]),
                    typenames = [Template_Argument(name = "S")]),
            Class(name = "Cls_T_Int_3", children = [
                Member(name = "ar", ctype = Array(
                    ctype = Type_Reference(name = Identifier(["Capdpa", "int"])),
                    size = 3))],
                instanceof = (["Capdpa", "Cls"], [Type_Literal(name=Identifier(["Capdpa", "int"]),value=3)])),
            Namespace(name = "Dummy", children = [
                Variable(name = "c3", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Cls"]), arguments=[
                    Type_Literal(name=Identifier(["Capdpa", "int"]),value=3)]))])])
        result = CXX("tests/data/convert/test_array_template_2.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_template_typedef(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=
                Class(name = "Container", children = [
                    Member(name = "value", ctype = Template_Argument(name = "T"))]),
                typenames = [Template_Argument(name = "T")]),
            Type_Definition(name = "Int_Container", reference = Type_Reference_Template(name = Identifier(["Capdpa", "Container"]),arguments=[
                Type_Reference(name = Identifier(["Capdpa", "int"]))]))])
        result = CXX("tests/data/convert/test_template_typedef.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_struct_type(self):
        expected = Namespace("Capdpa", children = [
            Class(name = "With_Struct", children = [
                Class(name = "Ws", children = [
                    Member(name = "x", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))]),
                Type_Definition(name = "Ws2", reference = None),
                Member(name = "value", ctype = Type_Reference(name = Identifier(["Capdpa", "With_Struct", "Ws", "Class"]), pointer = 1)),
                Member(name = "value2", ctype = Type_Reference(name = Identifier(["Capdpa", "With_Struct", "Ws2", "Class"]), pointer = 1))])])
        result = CXX("tests/data/convert/test_class_with_struct_type.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def EXCLUDE_test_class_template(self):
        expected = Namespace("Capdpa", children = [
            Class(name = "Base"),
            Class(name = "Template", children = [
                Constructor(parameters = [
                    Argument(name = "other", ctype =
                        Type_Reference(name = Identifier(["Capdpa", "Template"]), reference=True))],
                )])])
        result = CXX("tests/data/convert/test_class_template.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_typedef(self):
        expected = Namespace(name="Capdpa", children=[
            Namespace(name="With_typedef", children=[
                Type_Definition(name="u8", reference=Type_Reference(name=Identifier(name=["Capdpa", "unsigned_char"]))),
                Type_Definition(name="i32", reference=Type_Reference(name=Identifier(name=["Capdpa", "int"])))])])
        result = CXX("tests/data/convert/test_namespace_with_typedef.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_typedef(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Typedef", children = [
                Type_Definition(name = "i32", reference = Type_Reference(name = Identifier(["Capdpa", "int"])))]),
            Class(name = "Use_Typedef", children = [
                Member(name = "value", ctype=Type_Reference(Identifier(["Capdpa", "With_Typedef", "i32"])))])])
        result = CXX("tests/data/convert/test_class_with_typedef.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_enum_declaration(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Enum_Decl", children = [
                Enum(name = "E_t", children = [
                    Constant(name = "A", value = 0),
                    Constant(name = "B", value = 1)],
                        ctype = Type_Reference(name = Identifier(["Capdpa", "unsigned_int"]))),
                Member(name = "e", ctype=Type_Reference(Identifier(["Capdpa", "With_Enum_Decl", "E_t"])))
            ])])
        result = CXX("tests/data/convert/test_enum_declaration.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def EXCLUDE_test_function_pointer(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "With_Fptr", children = [
                Member(name = "func", ctype = Function_Reference()),
                Method(name = "set_func", parameters = [
                    Argument(name = "func", ctype = Function_Reference())]),
                Member(name = "member", ctype = Function_Reference(parameters = [
                    Argument(name = "This", ctype = Type_Reference(name = Identifier(["Capdpa", "With_Fptr"]), reference=True))]))
                ])])
        result = CXX("tests/data/convert/test_function_pointer.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def EXCLUDE_test_template_function_pointer(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=Class(name="With_Fptr", children = [
                Member(name = "func", ctype = Function_Reference(parameters = [
                    Argument(name = "This", ctype = Template_Argument(name="T"))])),
                Method(name = "set_func", parameters = [
                    Argument(name = "func", ctype = Function_Reference(parameters = [
                        Argument(name = "This", ctype = Template_Argument(name="T"))]))
                    ])
                ]), typenames = [Template_Argument(name = "T")])
            ])
        result = CXX("tests/data/convert/test_template_function_pointer.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_template_non_type(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=Class(name = "Tnt", children = [
                Member(name = "S", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))]),
                typenames = [Template_Argument(name = "Size")]),
            Class(name = "Tnt_T_Int_5", children = [
                Member(name = "S", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))],
                instanceof = (['Capdpa', 'Tnt'], [Type_Literal(constant=False,name=Identifier(name=['Capdpa', 'int']),pointer=0,reference=False,value=5)])),
            Class(name = "Tnt5", children = [
                Member(name = "t5", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Tnt"]), arguments = [
                    Type_Literal(name = Identifier(["Capdpa", "int"]), value = 5)]))],
                    instanceof = None)
            ])
        result = CXX("tests/data/convert/test_template_non_type.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_variadic_template(self):
        expected = Namespace(name = "Capdpa", children = [
            Template(entity=Class(name = "Templ", children = [
                Constructor(),
                Member(name = "element1", ctype = Template_Argument(name = "A")),
                Member(name = "element2", ctype = Template_Argument(name = "B"))
                ]), typenames = [
                    Template_Argument(name = "A"), Template_Argument(name = "B")]),
            Class(name = "Templ_T_Char_Int", children = [
                Constructor(),
                Member(name = "element1", ctype = Type_Reference(Identifier(["Capdpa", "char"]))),
                Member(name = "element2", ctype = Type_Reference(Identifier(["Capdpa", "int"])))],
                instanceof=(['Capdpa', 'Templ'], [Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'char']),pointer=0,reference=False),
                                                  Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'int']),pointer=0,reference=False)])),
            Class(name = "Templ_T_Char_Char", children = [
                Constructor(),
                Member(name = "element1", ctype = Type_Reference(Identifier(["Capdpa", "char"]))),
                Member(name = "element2", ctype = Type_Reference(Identifier(["Capdpa", "char"])))],
                instanceof=(['Capdpa', 'Templ'], [Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'char']),pointer=0,reference=False),
                                                  Type_Reference(constant=False,name=Identifier(name=['Capdpa', 'char']),pointer=0,reference=False)])),
            Template(entity=Class(name = "Var", children = [
                Constructor(),
                Member(name = "element1", ctype = Type_Reference(Identifier(["Capdpa", "int"])))]),
                typenames = [Template_Argument(name = "Ts", variadic=True)]),
            Class(name = "Var_T_", children = [
                Constructor(),
                Member(name = "element1", ctype = Type_Reference(Identifier(["Capdpa", "int"])))],
                instanceof=(['Capdpa', 'Var'], [])),
            Class(name = "Cls", children = [
                Constructor(),
                Method(name = "bar", parameters = [
                    Argument(name = "p1", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Templ"]), arguments = [
                        Type_Reference(name = Identifier(["Capdpa", "char"])),
                        Type_Reference(name = Identifier(["Capdpa", "int"]))])),
                    Argument(name = "p2", ctype = Type_Reference(Identifier(["Capdpa", "char"])))],
                    return_type = Type_Reference(Identifier(["Capdpa", "int"]))),
                Method(name = "foo", parameters = [
                    Argument(name = "p1", ctype = Type_Reference(Identifier(["Capdpa", "int"]))),
                    Argument(name = "p2", ctype = Type_Reference(Identifier(["Capdpa", "char"])))],
                    return_type = Type_Reference(Identifier(["Capdpa", "int"]))),
                Method(name = "baz", parameters = [
                    Argument(name = "p1", ctype = Type_Reference_Template(Identifier(["Capdpa", "Templ"]), arguments = [
                        Type_Reference(name = Identifier(["Capdpa", "char"])),
                        Type_Reference(name = Identifier(["Capdpa", "int"]))])),
                    Argument(name = "p2", ctype = Type_Reference_Template(Identifier(["Capdpa", "Templ"]), arguments = [
                        Type_Reference(name = Identifier(["Capdpa", "char"])),
                        Type_Reference(name = Identifier(["Capdpa", "char"]))]))],
                    return_type = Type_Reference(Identifier(["Capdpa", "int"]))),
                Method(name = "var", parameters = [
                    Argument(name = "p1", ctype = Type_Reference_Template(Identifier(["Capdpa", "Var"]), arguments = [])),
                    Argument(name = "p2", ctype = Type_Reference(Identifier(["Capdpa", "char"])))],
                    return_type = Type_Reference(Identifier(["Capdpa", "int"])))])])
        result = CXX("tests/data/convert/test_variadic_template.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def EXCLUDE_test_const_ref_function(self):
        expected = Namespace("Capdpa", children = [
            Class(name = "Cr", children = [
                Method(name = "method_with_function_parameter_const_ref", parameters = [
                    Argument(name = "arg1", ctype = Function_Reference(parameters = [
                        Argument(name = "arg1", ctype = Type_Reference(Identifier(["Capdpa", "int"]), reference=True, constant=True))]))])])])
        result = CXX("tests/data/convert/test_const_ref.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_export_method(self):
        expected = Namespace("Capdpa", children = [
                Class(name = "Cls", children = [
                    Method(name = "method", parameters = [
                        Argument("param", Type_Reference(Identifier(["Capdpa", "int"])))],
                        return_type = Type_Reference(Identifier(["Capdpa", "int"])),
                        export = True)])])
        result = CXX("tests/data/convert/test_export_method.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_constants_are_const(self):
        expected = Namespace (name = "Capdpa",
                              children = [Namespace(name = "Constants", children = [
                                              Variable (name = "constval",
                                                        ctype = Type_Reference(name = Identifier(["Capdpa", "int"]),
                                                                               constant = True,
                                                                               reference = False))])])
        result = CXX("tests/data/convert/test_constants_are_const.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_partial_template_specialization(self):
        result = CXX("tests/data/convert/test_partial_template_specialization.h").ToIR(project="Capdpa")

    def test_private_nested_class(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "Outer", children = [
                Class(name = "Inner", children = [
                    Member(name = "i", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))],
                    public = False),
                Member(access="private",constant=False,ctype=Type_Reference(constant=False,name=Identifier(name=["Capdpa", "Outer", "Inner"]),pointer=0,reference=False),name="inner"),
                Member(name = "o", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))])])
        result = CXX("tests/data/convert/test_private_nested_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_type_ref(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "Tr"),
            Template(entity = Class(name = "Tt"),
                typenames = [
                    Template_Argument(name = "T1"),
                    Template_Argument(name = "T2"),
                    Template_Argument(name = "T3"),
                    Template_Argument(name = "T4"),
                    Template_Argument(name = "T5"),
                    Template_Argument(name = "T6"),
                    Template_Argument(name = "T7")]),
            Class(name = "Tt_T_Tr_Int_Tr_Int_4_Tr_Char_T_Bool_True", instanceof=(
                ["Capdpa", "Tt"], [
                    Type_Reference(name=Identifier(["Capdpa", "Tr", "Class"])),
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "Tr", "Class"])),
                    Type_Literal(name=Identifier(["Capdpa", "int"]), value=4),
                    Type_Reference(name=Identifier(["Capdpa", "Tr", "Class"])),
                    Type_Literal(name=Identifier(["Capdpa", "char"]), value='t'),
                    Type_Literal(name=Identifier(["Capdpa", "bool"]), value="true")])),
            Class(name = "T", children = [
                Member(name = "t", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Tt"]), arguments = [
                    Type_Reference(name=Identifier(["Capdpa", "Tr", "Class"])),
                    Type_Reference(name=Identifier(["Capdpa", "int"])),
                    Type_Reference(name=Identifier(["Capdpa", "Tr", "Class"])),
                    Type_Literal(name=Identifier(["Capdpa", "int"]), value=4),
                    Type_Reference(name=Identifier(["Capdpa", "Tr", "Class"])),
                    Type_Literal(name=Identifier(["Capdpa", "char"]), value='t'),
                    Type_Literal(name=Identifier(["Capdpa", "bool"]), value="true")]))])])
        result = CXX("tests/data/convert/test_type_ref.h").ToIR(project="Capdpa")
        self.check(result, expected)

if __name__ == '__main__':
    unittest.main()
