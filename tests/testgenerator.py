# -*- coding: utf-8 -*-

import unittest
from capdpa import *
from capdpa_test import *

class GenerateConstant(Capdpa_Test):

    def test_simple_constant(self):
        result = Constant("whats_the_question", 42).AdaSpecification()
        self.check(result, "Whats_The_Question : constant := 42")

    def test_simple_negative_constant(self):
        result = Constant("negative", -42).AdaSpecification()
        self.check(result, "Negative : constant := -42")

    def test_identifier_escape_begin(self):
        result = Constant("_invalid", 0).AdaSpecification()
        self.check(result, "X_Invalid : constant := 0")

    def test_identifier_escape_begin_digit(self):
        result = Constant("42invalid", 0).AdaSpecification()
        self.check(result, "X42invalid : constant := 0")

    def test_identifier_escape_end(self):
        result = Constant("invalid_", 0).AdaSpecification()
        self.check(result, "Invalid_X : constant := 0")

    def test_identifier_double_underscore(self):
        result = Constant("inv__alid", 0).AdaSpecification()
        self.check(result, "Inv_X_Alid : constant := 0")

    def test_identifier_multiple_underscores(self):
        result = Constant("inv____alid", 0).AdaSpecification()
        self.check(result, "Inv_X_X_X_Alid : constant := 0")

    def test_identifier_reserved_word1(self):
        result = Constant("begin", 0).AdaSpecification()
        self.check(result, "X_Begin : constant := 0")

    def test_identifier_reserved_word2(self):
        result = Constant("while", 0).AdaSpecification()
        self.check(result, "X_While : constant := 0")

    def test_unsupported_character(self):
        result = Constant("Thüringer_Klöße", 0).AdaSpecification()
        self.check(result, "Thc3bcringer_Klc3b6c39fe : constant := 0")

    def test_class_simple(self):
        expected_class = self.load("test_class_simple.txt")
        expected_package = self.load("test_package_foo.txt")

        result = Namespace(name = "foo", children = [
            Class(name = "brabbel", children = [
                Constructor(symbol = "SYM_FIXME")]
                      )]).AdaSpecification()

        self.check(result[0], expected_package)
        self.check(result[1], expected_class)

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

        self.check(result[2], expected)
        self.check(result[1], foo)
        self.check(result[0], bar)

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

        self.check(result[2], expected)
        self.check(result[1], foo)
        self.check(result[0], bar)

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

        self.check(result[2], expected)
        self.check(result[1], foo)
        self.check(result[0], bar)

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

        self.check(result[2], expected)
        self.check(result[1], foo)
        self.check(result[0], bar)

    def test_constant(self):
        self.check(Constant("someconstant", 123).AdaSpecification(), "Someconstant : constant := 123")

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

        self.check(result[2], expected)
        self.check(result[1], foo)
        self.check(result[0], bar)

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

        self.check(result[2], expected)
        self.check(result[1], foo)
        self.check(result[0], bar)

    def test_empty_namespace(self):
        expected = self.load("test_empty_namespace.txt")
        blah = self.load("test_package_blah.txt")

        result = Namespace(name="blah", children=[Namespace(name = "blubb")]).AdaSpecification()

        self.check(result[1], expected)
        self.check(result[0], blah)

    def test_enumeration(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1"),
                                   Constant(name = "elem2")]).AdaSpecification()
        self.check(result, "type Foo is (Elem1, Elem2)")

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
                        Constant("Elem21"),
                        Constant("Elem22"),
                        Constant("Elem23")])]
                    )])]).AdaSpecification()

        self.check(result[2], expected)
        self.check(result[1], foo)
        self.check(result[0], bar)

    def test_enum_representation(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1", value = 50),
                                   Constant(name = "elem2", value = 1234)]).AdaRepresentation()
        self.check(result, "for Foo use (Elem1 => 50, Elem2 => 1234)")

    def test_class_multiple_constructors(self):
        expected = self.load("test_class_multiple_constructors.txt")
        foo = self.load("test_package_foo.txt")

        result = Namespace(name = "foo", children = [
            Class(name = "brabbel", children = [
                Constructor(symbol = "SYM_FIXME"),
                Constructor(symbol = "SYM_FIXME", parameters = [
                    Variable(name = "arg", ctype = Type_Reference(name=Identifier(["integer"])))])]
                )]).AdaSpecification()

        self.check(result[1], expected)
        self.check(result[0], foo)
