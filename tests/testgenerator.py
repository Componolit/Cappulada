#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if __name__ == '__main__':
    sys.path.append (".")

import unittest
from capdpa import *
from capdpa_test import *

class GenerateConstant(Capdpa_Test):

    def test_simple_constant(self):
        result = Constant("whats_the_question", 42).AdaSpecification()
        self.check(result, "Whats_The_Question : constant := 42;")

    def test_simple_negative_constant(self):
        result = Constant("negative", -42).AdaSpecification()
        self.check(result, "Negative : constant := -42;")

    def test_identifier_escape_begin(self):
        result = Constant("_invalid", 0).AdaSpecification()
        self.check(result, "X_Invalid : constant := 0;")

    def test_identifier_escape_begin_digit(self):
        result = Constant("42invalid", 0).AdaSpecification()
        self.check(result, "X42invalid : constant := 0;")

    def test_identifier_escape_end(self):
        result = Constant("invalid_", 0).AdaSpecification()
        self.check(result, "Invalid_X : constant := 0;")

    def test_identifier_double_underscore(self):
        result = Constant("inv__alid", 0).AdaSpecification()
        self.check(result, "Inv_X_Alid : constant := 0;")

    def test_identifier_multiple_underscores(self):
        result = Constant("inv____alid", 0).AdaSpecification()
        self.check(result, "Inv_X_X_X_Alid : constant := 0;")

    def test_identifier_reserved_word1(self):
        result = Constant("begin", 0).AdaSpecification()
        self.check(result, "X_Begin : constant := 0;")

    def test_identifier_reserved_word2(self):
        result = Constant("while", 0).AdaSpecification()
        self.check(result, "X_While : constant := 0;")

    def test_unsupported_character(self):
        result = Constant("Thüringer_Klöße", 0).AdaSpecification()
        self.check(result, "Thc3bcringer_Klc3b6c39fe : constant := 0;")

    def test_class_simple(self):
        expected_class = self.load("generator/test_package_foo_brabbel.txt")

        data = Namespace (name = "Capdpa", children = [
            Namespace(name = "foo", children = [
                Class(name = "brabbel", children = [Constructor()])])])

        result = data.children[0].AdaSpecification()
        self.check(result[0].Text(), expected_class)

    def test_class_elements(self):
        expected = self.load("generator/test_class_with_elements.txt")

        data = Namespace(name = "bar", children=[
            Namespace(name = "foo", children=[
                Class(name = "brabbel",children = [
                    Constructor(),
                    Member("field1", Type_Reference(Identifier(["Capdpa", "int"]))),
                    Member("field2", Type_Reference(Identifier(["Capdpa", "long"])))]
                    )])])

        data = Namespace(name = "Capdpa", children = [data])
        result = data.children[0].AdaSpecification()

        self.check(result[1].Text(), expected)

    def test_class_elements_external_types(self):
        expected = self.load("generator/test_class_with_external_types.txt")

        data = Namespace(name = "bar", children = [
            Namespace(name = "foo", children=[
                Class(name = "brabbel", children = [
                    Constructor(),
                    Member("field1", Type_Reference(Identifier(["Capdpa", "bar", "baz", "my_type"]))),
                    Member("field2", Type_Reference(Identifier(["Capdpa", "bar", "foo", "brabbel", "local_type"]))),
                    Member("field3", Type_Reference(Identifier(["Capdpa", "bar", "foo", "blub", "some_type"])))]
                    )])])

        data = Namespace(name = "Capdpa", children = [data])
        result = data.children[0].AdaSpecification()

        self.check(result[1].Text(), expected)

    def test_class_elements_local_types(self):
        bar = self.load("generator/test_package_bar.txt")
        expected = self.load("generator/test_class_with_local_types.txt")

        data = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "brabbel", children = [
                    Constructor(),
                    Member("field1", Type_Reference(Identifier(["Capdpa", "bar", "baz", "my_type"]))),
                    Member("field2", Type_Reference(Identifier(["Capdpa", "bar", "foo", "brabbel", "local_type"]))),
                    Member("field3", Type_Reference(Identifier(["Capdpa", "bar", "foo", "blub", "some_type"]))),
                    Member("field4", Type_Reference(Identifier(["Capdpa", "bar", "foo", "brabbel", "some_type"]))),
                    ])])])

        data = Namespace(name = "Capdpa", children = [data])
        result = data.children[0].AdaSpecification()

        self.check(result[0].Text(), bar)
        self.check(result[1].Text(), expected)

    def test_class_functions_with_return_type(self):

        bar = self.load("generator/test_package_bar.txt")
        expected = self.load("generator/test_class_functions_with_return_type.txt")

        data = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "brabbel", children = [
                    Constructor(),
                    Member("field1", Type_Reference(Identifier(["Capdpa", "bar", "baz", "my_type"]))),
                    Member("field2", Type_Reference(Identifier(["Capdpa", "bar", "foo", "brabbel", "local_type"]))),
                    Member("field3", Type_Reference(Identifier(["Capdpa", "bar", "foo", "blub", "some_type"]))),
                    Method(name = "do_something", parameters = [
                        Argument("param1", Type_Reference(Identifier(["Capdpa", "foo", "bar"]))),
                        Argument("param2", Type_Reference(Identifier(["Capdpa", "foo", "baz"])))],
                        return_type = Type_Reference(Identifier(["Capdpa", "Blah", "Some_Type"])))]
                        )])])

        data = Namespace(name = "Capdpa", children = [data])
        result = data.children[0].AdaSpecification()

        self.check(result[0].Text(), bar)
        self.check(result[1].Text(), expected)

    def test_constant(self):
        self.check(Constant("someconstant", 123).AdaSpecification(), "Someconstant : constant := 123;")

    def test_namespace_with_constants(self):

        data = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Namespace(name = "namespace", children = [
                    Constant(name = "constant1", value = 5),
                    Constant(name = "constant2", value = 42)]
                    )])])

        data = Namespace(name = "Capdpa", children = [data])
        result = data.children[0].AdaSpecification()

        self.check(result[0].Text(), self.load("generator/test_package_bar.txt"))
        self.check(result[1].Text(), self.load("generator/test_package_bar_foo.txt"))

    def test_class_with_constants(self):

        data = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "class", children = [
                    Constructor(),
                    Constant(name = "constant1", value = 5),
                    Constant(name = "constant2", value = 42)]
                    )])])

        data = Namespace(name = "Capdpa", children = [data])
        result = data.children[0].AdaSpecification()

        self.check(result[0].Text(), self.load("generator/test_package_bar.txt"))
        self.check(result[1].Text(), self.load("generator/test_package_bar_foo_class_const.txt"))

    def test_empty_namespace(self):
        expected = self.load("generator/test_empty_namespace.txt")
        blah = self.load("generator/test_package_blah.txt")

        result = Namespace(name="blah", children=[Namespace(name = "blubb")]).AdaSpecification()

        self.check(result[1].Text(), expected)
        self.check(result[0].Text(), blah)

    def test_enumeration(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1", value = 0),
                                   Constant(name = "elem2", value = 1)]).AdaSpecification()
        self.check(result, "type Foo is (Elem1, Elem2);\nfor Foo use (Elem1 => 0, Elem2 => 1);")

    def test_class_with_enum(self):

        data = Namespace(name = "bar", children=[
            Namespace(name = "foo", children=[
                Class(name = "class", children = [
                    Constructor(),
                    Enum(name = "enum1", children = [
                        Constant("Elem11", 5),
                        Constant("Elem12", 6)]),
                    Enum(name = "enum2", children = [
                        Constant("Elem21", 0),
                        Constant("Elem22", 1),
                        Constant("Elem23", 2)])]
                    )])])

        data = Namespace(name = "Capdpa", children=[data])
        result = data.children[0].AdaSpecification()

        self.check(result[0].Text(), self.load("generator/test_package_bar.txt"))
        self.check(result[1].Text(), self.load("generator/test_package_bar_foo_class.txt"))

    def test_enum_representation(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1", value = 50),
                                   Constant(name = "elem2", value = 1234)]).AdaSpecification()
        self.check(result, "type Foo is (Elem1, Elem2);\nfor Foo use (Elem1 => 50, Elem2 => 1234);")

    def test_class_multiple_constructors(self):
        expected = self.load("generator/test_class_multiple_constructors.txt")

        data = Namespace(name = "foo", children = [
            Class(name = "brabbel", children = [
                Constructor(),
                Constructor(parameters = [
                    Argument(name = "arg", ctype = Type_Reference(name=Identifier(["Capdpa", "integer"])))])]
                )])

        data = Namespace(name = "Capdpa", children = [data])
        result = data.children[0].AdaSpecification()

        self.check(result[0].Text(), expected)

    def test_type_template_one_arg(self):
        result = Type_Reference_Template(Identifier(["Capdpa", "Class"]),
                arguments=[Type_Reference(name=Identifier(["Capdpa", "Int"]))]).AdaSpecification()
        self.check(result, "Capdpa.Class_T_Int.Class")

    def test_type_template_two_args(self):
        result = Type_Reference_Template(Identifier(["Capdpa", "Class"]),
                arguments=[
                    Type_Reference(name=Identifier(["Capdpa", "Int"])),
                    Type_Reference(name=Identifier(["Capdap", "Char"]))]).AdaSpecification()
        self.check(result, "Capdpa.Class_T_Int_Char.Class")

    def test_type_template_template_arg(self):
        result = Type_Reference_Template(name=Identifier(["Capdpa", "Class"]),
                arguments=[
                    Type_Reference_Template(name=Identifier(["Capdpa", "Tclass"]),
                        arguments=[
                            Type_Reference(name=Identifier(["Capdpa", "Int"]))])]).AdaSpecification()
        self.check(result, "Capdpa.Class_T_Tclass_T_Int.Class")

    def test_inheritance_simple(self):
        result = Namespace(name="Capdpa", children=[
            Class(name="Simple", children=[
                Member(name="A", ctype=Type_Reference(name=Identifier(["Capdpa", "Int"])))
                ]),
            Class(name="Inherit_Simple", children=[
                Class_Reference(name=Identifier(["Capdpa", "Simple"])),
                Member(name="B", ctype=Type_Reference(name=Identifier(["Capdpa", "Int"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_inherit_simple.txt"))

    def test_class_with_virtual(self):
        result = Namespace(name="Capdpa", children=[
            Class(name = "With_Virtual", children = [
                Method(name = "Foo", virtual = True)])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_base_with_virtual.txt"))

    def test_inherit_from_virtual(self):
        result = Namespace(name="Capdpa", children=[
            Class(name = "With_Virtual", children = [
                Method(name = "Foo", virtual = True)]),
            Class(name = "From_Virtual",
                children = [
                    Class_Reference(name=Identifier(["Capdpa", "With_Virtual"])),
                    Member(name = "V", ctype = Type_Reference(name = Identifier(["Capdpa", "Int"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_inherit_from_virtual.txt"))

    def test_nested_package(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "Outer", children = [
                Class(name = "Inner", children = []),
                Member(name = "field", ctype = Type_Reference(name = Identifier(["Capdpa", "Outer", "Inner", "Class"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_nested_package.txt"))

    def test_pointer_member(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Pointer", children = [
                Member(name = "P", ctype = Type_Reference(name = Identifier(["Capdpa", "Int"]), pointer = 1))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_pointer_member.txt"))

    def test_pointer_depth(self):
        var = Variable(name="var", ctype = Type_Reference(name = Identifier(["Test"]), pointer = 2))
        self.assertRaises(ValueError, var.AdaSpecification)

    def test_reference_member(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Reference", children = [
                Member(name = "R", ctype = Type_Reference(name = Identifier(["Capdpa", "Int"]), reference = True))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_reference_member.txt"))

    def test_spec_file_name(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "Child1"),
            Namespace(name = "Child2", children = [
                Namespace(name = "Child3", children = [
                    Class(name = "Grandchild")])])]).AdaSpecification()
        self.check(result[0].FileName(), "capdpa.ads")
        self.check(result[1].FileName(), "capdpa-child2.ads")
        self.check(result[2].FileName(), "capdpa-child2-child3.ads")

    def test_enum_member(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Enum", children = [
                Enum(name = "E_t", children = [
                    Constant(name = "A", value = 0),
                    Constant(name = "B", value = 1)],
                    ctype = Type_Reference(name=Identifier(["Capdpa", "unsigned_int"]))),
                Member(name = "E", ctype=Type_Reference(name = Identifier(["Capdpa", "With_Enum", "E_t"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_enum_member.txt"))

    def test_function_pointer_base(self):
        self.check(Function_Reference(pointer=1).AdaSpecification(), "access procedure (This : Class)")
        self.check(Function_Reference(
            parameters=[Argument(name = "a", ctype=Type_Reference(name=Identifier(["Capdpa", "Int"]))),
                        Argument(name = "b", ctype=Type_Reference(name=Identifier(["A", "Class"])))],
            pointer=1).AdaSpecification(),
            "access procedure (This : Class; A : Capdpa.Int; B : A.Class)")
        self.check(Function_Reference(
            pointer=1,
            return_type=Type_Reference(name=Identifier(["Capdpa", "Int"]))).AdaSpecification(),
                "access function (This : Class) return Capdpa.Int")
        self.check(Function_Reference(
            pointer=1,
            return_type=Type_Reference(name=Identifier(["Capdpa", "Int"])),
            parameters=[Argument(name="X", ctype=Type_Reference(name=Identifier(["Capdpa", "Int"])))]
            ).AdaSpecification(), "access function (This : Class; X : Capdpa.Int) return Capdpa.Int")
        self.check(Function_Reference(
            pointer=1,
            return_type=Function_Reference(
                pointer=1,
                return_type=Function_Reference(
                    pointer=1,
                    return_type=Function_Reference()))).AdaSpecification(),
            "access function (This : Class) return access function (This : Class) return access function (This : Class) return access procedure (This : Class)")

    def test_function_pointer(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Fptr", children = [
                Member(name = "func", ctype = Function_Reference(pointer=1)),
                Method(name = "set_func", parameters = [
                    Argument(name = "func", ctype = Function_Reference(pointer=1))])
                ])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_function_pointer.txt"))

    def test_class_with_array(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Array", children = [
                Member(name = "ar", ctype = Array(ctype = Type_Reference(name = Identifier(["Capdpa", "Int"])), size=5))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_class_with_array.txt"))

    def test_template_with_array(self):
        result = Namespace(name = "Capdpa", children = [
            Template(entity=
                Class(name = "Template_With_Array", children = [
                    Member(name = "var", ctype = Array(
                        ctype = Type_Reference(name = Identifier(["Capdpa", "int"])),
                        size = Template_Argument(name = "Size")))]),
                    typenames = [Template_Argument(name = "Size")]
                    ),
            Class(name = "Template_With_Array_T_X5", children = [
                Member(name = "var", ctype = Array(
                    ctype = Type_Reference(name = Identifier(["Capdpa", "int"])),
                    size = 5))],
                instanceof = (["Capdpa", "Template_With_Array"], [Type_Literal(value=5)])),
            Class(name = "With_Array_5", children = [
                Member(name = "twa", ctype = Type_Reference_Template(name = Identifier(["Capdpa", "Template_With_Array"]), arguments = [
                    Type_Literal(value = 5)]))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_template_with_array.txt"))

    def test_private_reference_member(self):
        result = Class(name = "Class_Priv_Ref", children = [
                Member(name = "ref_member",
                       ctype = Type_Reference(name = Identifier(["Capdpa", "int"]), reference = True),
                       access = "private")]).AdaSpecification()
        self.check(result, self.load("generator/test_private_reference_member.txt"))

    def test_constants_are_const(self):
        result = Namespace (name = "Capdpa",
                            children = [Namespace(name = "Constants", children = [
                                            Variable(name = "constval",
                                                     ctype = Type_Reference(name = Identifier(["Capdpa", "int"]),
                                                                            constant = True,
                                                                            reference = False))])]).AdaSpecification()
        self.check(result[1].Text(), self.load("test_constants_are_const.ads"))

    def test_private_nested_class(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "Outer", children = [
                Class(name = "Inner", children = [
                    Member(name = "i", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))],
                    public = False),
                Member(access="private",constant=False,ctype=Type_Reference(constant=False,name=Identifier(name=["Capdpa", "Outer", "Inner"]),pointer=0,reference=False),name="local"),
                Member(name = "o", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("generator/test_private_nested_class.txt"))

if __name__ == '__main__':
    unittest.main()
