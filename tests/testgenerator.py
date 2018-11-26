# -*- coding: utf-8 -*-

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
        expected_class = self.load("test_class_simple.txt")
        expected_package = self.load("test_package_foo.txt")

        result = Namespace(name = "foo", children = [
            Class(name = "brabbel", children = [
                Constructor(symbol = "SYM_FIXME")]
                      )]).AdaSpecification()

        self.check(result[0].Text(), expected_package)
        self.check(result[1].Text(), expected_class)

    def test_class_elements(self):
        expected = self.load("test_class_with_elements.txt")
        bar = self.load("test_package_bar.txt")
        foo = self.load("test_package_bar_foo.txt")

        result = Namespace(name = "bar", children=[
            Namespace(name = "foo", children=[
                Class(name = "brabbel",children = [
                    Constructor(symbol = "SYM_FIXME"),
                    Variable("field1", Type_Reference(Identifier(["int"]))),
                    Variable("field2", Type_Reference(Identifier(["long"])))]
                    )])]).AdaSpecification()

        self.check(result[2].Text(), expected)
        self.check(result[1].Text(), foo)
        self.check(result[0].Text(), bar)

    def test_class_elements_external_types(self):
        expected = self.load("test_class_with_external_types.txt")
        bar = self.load("test_package_bar.txt")
        foo = self.load("test_package_bar_foo.txt")

        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children=[
                Class(name = "brabbel", children = [
                    Constructor(symbol="SYM_FIXME"),
                    Variable("field1", Type_Reference(Identifier(["bar", "baz", "my_type"]))),
                    Variable("field2", Type_Reference(Identifier(["local_type"]))),
                    Variable("field3", Type_Reference(Identifier(["bar", "foo", "blub", "some_type"])))]
                    )])]).AdaSpecification()

        self.check(result[2].Text(), expected)
        self.check(result[1].Text(), foo)
        self.check(result[0].Text(), bar)

    def test_class_elements_local_types(self):
        expected = self.load("test_class_with_local_types.txt")
        bar = self.load("test_package_bar.txt")
        foo = self.load("test_package_bar_foo.txt")

        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "brabbel", children = [
                    Constructor(symbol="SYM_FIXME"),
                    Variable("field1", Type_Reference(Identifier(["bar", "baz", "my_type"]))),
                    Variable("field2", Type_Reference(Identifier(["local_type"]))),
                    Variable("field3", Type_Reference(Identifier(["bar", "foo", "blub", "some_type"]))),
                    Variable("field4", Type_Reference(Identifier(["bar", "foo", "brabbel", "some_type"]))),
                    ])])]).AdaSpecification()

        self.check(result[2].Text(), expected)
        self.check(result[1].Text(), foo)
        self.check(result[0].Text(), bar)

    def test_class_functions_with_return_type(self):
        expected = self.load("test_class_functions_with_return_type.txt")
        bar = self.load("test_package_bar.txt")
        foo = self.load("test_package_bar_foo.txt")

        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "brabbel", children = [
                    Constructor(symbol="SYM_FIXME"),
                    Variable("field1", Type_Reference(Identifier(["bar", "baz", "my_type"]))),
                    Variable("field2", Type_Reference(Identifier(["local_type"]))),
                    Variable("field3", Type_Reference(Identifier(["bar", "foo", "blub", "some_type"]))),
                    Function(name = "do_something", symbol = "this_function_has_a_funny_symbol", parameters = [
                        Variable("param1", Type_Reference(Identifier(["foo", "bar"]))),
                        Variable("param2", Type_Reference(Identifier(["foo", "baz"])))],
                        return_type = Type_Reference(Identifier(["Blah", "Some_Type"])))]
                        )])]).AdaSpecification()

        self.check(result[2].Text(), expected)
        self.check(result[1].Text(), foo)
        self.check(result[0].Text(), bar)

    def test_constant(self):
        self.check(Constant("someconstant", 123).AdaSpecification(), "Someconstant : constant := 123;")

    def test_namespace_with_constants(self):
        expected = self.load("test_namespace_with_constants.txt")
        bar = self.load("test_package_bar.txt")
        foo = self.load("test_package_bar_foo.txt")

        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Namespace(name = "namespace", children = [
                    Constant(name = "constant1", value = 5),
                    Constant(name = "constant2", value = 42)]
                    )])]).AdaSpecification()

        self.check(result[2].Text(), expected)
        self.check(result[1].Text(), foo)
        self.check(result[0].Text(), bar)

    def test_class_with_constants(self):
        expected = self.load("test_class_with_constants.txt")
        bar = self.load("test_package_bar.txt")
        foo = self.load("test_package_bar_foo.txt")

        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "class", children = [
                    Constructor(symbol="symbol_404"),
                    Constant(name = "constant1", value = 5),
                    Constant(name = "constant2", value = 42)]
                    )])]).AdaSpecification()

        self.check(result[2].Text(), expected)
        self.check(result[1].Text(), foo)
        self.check(result[0].Text(), bar)

    def test_empty_namespace(self):
        expected = self.load("test_empty_namespace.txt")
        blah = self.load("test_package_blah.txt")

        result = Namespace(name="blah", children=[Namespace(name = "blubb")]).AdaSpecification()

        self.check(result[1].Text(), expected)
        self.check(result[0].Text(), blah)

    def test_enumeration(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1", value = 0),
                                   Constant(name = "elem2", value = 1)]).AdaSpecification()
        self.check(result, "type Foo is (Elem1, Elem2);\nfor Foo use (Elem1 => 0, Elem2 => 1);")

    def test_class_with_enum(self):
        expected = self.load("test_class_with_enum.txt")
        bar = self.load("test_package_bar.txt")
        foo = self.load("test_package_bar_foo.txt")

        result = Namespace(name = "bar", children=[
            Namespace(name = "foo", children=[
                Class(name = "class", children = [
                    Constructor(symbol="symbol_404"),
                    Enum(name = "enum1", children = [
                        Constant("Elem11", 5),
                        Constant("Elem12", 6)]),
                    Enum(name = "enum2", children = [
                        Constant("Elem21", 0),
                        Constant("Elem22", 1),
                        Constant("Elem23", 2)])]
                    )])]).AdaSpecification()

        self.check(result[2].Text(), expected)
        self.check(result[1].Text(), foo)
        self.check(result[0].Text(), bar)

    def test_enum_representation(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1", value = 50),
                                   Constant(name = "elem2", value = 1234)]).AdaSpecification()
        self.check(result, "type Foo is (Elem1, Elem2);\nfor Foo use (Elem1 => 50, Elem2 => 1234);")

    def test_class_multiple_constructors(self):
        expected = self.load("test_class_multiple_constructors.txt")
        foo = self.load("test_package_foo.txt")

        result = Namespace(name = "foo", children = [
            Class(name = "brabbel", children = [
                Constructor(symbol = "SYM_FIXME"),
                Constructor(symbol = "SYM_FIXME", parameters = [
                    Variable(name = "arg", ctype = Type_Reference(name=Identifier(["integer"])))])]
                )]).AdaSpecification()

        self.check(result[1].Text(), expected)
        self.check(result[0].Text(), foo)

    def test_type_template_one_arg(self):
        result = Type_Reference_Template(Identifier(["Capdpa", "Class"]),
                arguments=[Type_Reference(name=Identifier(["Capdpa", "Int"]))]).AdaSpecification()
        self.check(result, "Capdpa.Class_T_Int")

    def test_type_template_two_args(self):
        result = Type_Reference_Template(Identifier(["Capdpa", "Class"]),
                arguments=[
                    Type_Reference(name=Identifier(["Capdpa", "Int"])),
                    Type_Reference(name=Identifier(["Capdap", "Char"]))]).AdaSpecification()
        self.check(result, "Capdpa.Class_T_Int_Char")

    def test_type_template_template_arg(self):
        result = Type_Reference_Template(name=Identifier(["Capdpa", "Class"]),
                arguments=[
                    Type_Reference_Template(name=Identifier(["Capdpa", "Tclass"]),
                        arguments=[
                            Type_Reference(name=Identifier(["Capdpa", "Int"]))])]).AdaSpecification()
        self.check(result, "Capdpa.Class_T_Tclass_T_Int")

    def test_inheritance_simple(self):
        result = Namespace(name="Capdpa", children=[
            Class(name="Simple", children=[
                Variable(name="A", ctype=Type_Reference(name=Identifier(["Int"])))
                ]),
            Class(name="Inherit_Simple", children=[
                Class_Reference(name=Identifier(["Capdpa", "Simple"])),
                Variable(name="B", ctype=Type_Reference(name=Identifier(["Int"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("test_capdpa.txt"))
        self.check(result[1].Text(), self.load("test_base_simple.txt"))
        self.check(result[2].Text(), self.load("test_inherit_simple.txt"))

    def test_class_with_virtual(self):
        result = Namespace(name="Capdpa", children=[
            Class(name = "With_Virtual", children = [
                Function(name = "Foo", symbol = "", virtual = True)])]).AdaSpecification()
        self.check(result[0].Text(), self.load("test_capdpa.txt"))
        self.check(result[1].Text(), self.load("test_base_with_virtual.txt"))

    def test_inherit_from_virtual(self):
        result = Namespace(name="Capdpa", children=[
            Class(name = "With_Virtual", children = [
                Function(name = "Foo", symbol = "", virtual = True)]),
            Class(name = "From_Virtual",
                children = [
                    Class_Reference(name=Identifier(["Capdpa", "With_Virtual"])),
                    Variable(name = "V", ctype = Type_Reference(name = Identifier(["Capdpa", "Int"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("test_capdpa.txt"))
        self.check(result[1].Text(), self.load("test_base_with_virtual.txt"))
        self.check(result[2].Text(), self.load("test_inherit_from_virtual.txt"))

    def test_nested_package(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "Outer", children = [
                Class(name = "Inner", children = []),
                Variable(name = "field", ctype = Type_Reference(name = Identifier(["Capdpa", "Outer", "Inner", "Class"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("test_capdpa.txt"))
        self.check(result[1].Text(), self.load("test_nested_package.txt"))

    def test_pointer_member(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Pointer", children = [
                Variable(name = "P", ctype = Type_Reference(name = Identifier(["Int"]), pointer = 1))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("test_capdpa.txt"))
        self.check(result[1].Text(), self.load("test_pointer_member.txt"))

    def test_pointer_depth(self):
        var = Variable(name="var", ctype = Type_Reference(name = Identifier(["Test"]), pointer = 2))
        self.assertRaises(ValueError, var.AdaSpecification)

    def test_reference_member(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Reference", children = [
                Variable(name = "R", ctype = Type_Reference(name = Identifier(["Int"]), reference = True))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("test_capdpa.txt"))
        self.check(result[1].Text(), self.load("test_reference_member.txt"))

    def test_spec_file_name(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "Child1"),
            Namespace(name = "Child2", children = [
                Class(name = "Grandchild")])]).AdaSpecification()
        self.check(result[0].FileName(), "capdpa.ads")
        self.check(result[1].FileName(), "capdpa-child1.ads")
        self.check(result[2].FileName(), "capdpa-child2.ads")
        self.check(result[3].FileName(), "capdpa-child2-grandchild.ads")

    def test_enum_member(self):
        result = Namespace(name = "Capdpa", children = [
            Class(name = "With_Enum", children = [
                Enum(name = "E_t", children = [
                    Constant(name = "A", value = 0),
                    Constant(name = "B", value = 1)]),
                Variable(name = "E", ctype=Type_Reference(name = Identifier(["Capdpa", "With_Enum", "E_t"])))])]).AdaSpecification()
        self.check(result[0].Text(), self.load("test_capdpa.txt"))
        self.check(result[1].Text(), self.load("test_enum_member.ads"))

    def test_class_with_array(self):
        self.fail("Handle array types (TypeKind.CONSTANTARRAY)")
