# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class GenerateConstant(unittest.TestCase):

    def test_simple_constant(self):
        result = Constant("whats_the_question", 42).AdaSpecification()
        self.assertTrue(result == "Whats_The_Question : constant := 42",
                        "Invalid constant: " + result)

    def test_simple_negative_constant(self):
        result = Constant("negative", -42).AdaSpecification()
        self.assertTrue(result == "Negative : constant := -42",
                        "Invalid constant: " + result)

    def test_identifier_escape_begin(self):
        result = Constant("_invalid", 0).AdaSpecification()
        self.assertTrue(result == "X_Invalid : constant := 0",
                        "Invalid constant: " + result)

    def test_identifier_escape_begin_digit(self):
        result = Constant("42invalid", 0).AdaSpecification()
        self.assertTrue(result == "X42invalid : constant := 0",
                        "Invalid constant: " + result)

    def test_identifier_escape_end(self):
        result = Constant("invalid_", 0).AdaSpecification()
        self.assertTrue(result == "Invalid_X : constant := 0",
                        "Invalid constant: " + result)

    def test_identifier_double_underscore(self):
        result = Constant("inv__alid", 0).AdaSpecification()
        self.assertTrue(result == "Inv_X_Alid : constant := 0",
                        "Invalid constant: " + result)

    def test_identifier_multiple_underscores(self):
        result = Constant("inv____alid", 0).AdaSpecification()
        self.assertTrue(result == "Inv_X_X_X_Alid : constant := 0",
                        "Invalid constant: " + result)

    def test_identifier_reserved_word1(self):
        result = Constant("begin", 0).AdaSpecification()
        self.assertTrue(result == "X_Begin : constant := 0",
                        "Invalid constant: " + result)

    def test_identifier_reserved_word2(self):
        result = Constant("while", 0).AdaSpecification()
        self.assertTrue(result == "X_While : constant := 0",
                        "Invalid constant: " + result)

    def test_unsupported_character(self):
        result = Constant("Thüringer_Klöße", 0).AdaSpecification()
        self.assertTrue(result == "Thc3bcringer_Klc3b6c39fe : constant := 0",
                        "Invalid constant: " + result)

    def test_class_simple(self):
        expected_class = open("tests/data/test_class_simple.txt", "r").read()
        expected_package = open("tests/data/test_package_foo.txt", "r").read()
        result = Namespace(name = "foo", children = [
            Class(name = "brabbel", children = [
                Constructor(symbol = "SYM_FIXME")]
                      )]).AdaSpecification()
        self.assertTrue(result[0] == expected_package, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + expected_package + "\n<<<")
        self.assertTrue(result[1] == expected_class, "Invalid class: >>>\n" + result[1] + "\n<<< expected: >>>\n" + expected_class + "\n<<<")

    def test_class_elements(self):
        expected = open("tests/data/test_class_with_elements.txt", "r").read()
        bar = open("tests/data/test_package_bar.txt", "r").read()
        foo = open("tests/data/test_package_bar_foo.txt", "r").read()
        result = Namespace(name = "bar", children=[
            Namespace(name = "foo", children=[
                Class(name = "brabbel",children = [
                    Constructor(symbol = "SYM_FIXME"),
                    Variable("field1", Type_Reference(Identifier(["int"]))),
                    Variable("field2", Type_Reference(Identifier(["long"])))]
                    )])]).AdaSpecification()
        self.assertTrue(result[2] == expected, "Invalid class: >>>\n" + result[2] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[1] == foo, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + foo + "\n<<<")
        self.assertTrue(result[0] == bar, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + bar + "\n<<<")

    def test_class_elements_external_types(self):
        expected = open("tests/data/test_class_with_external_types.txt", "r").read()
        bar = open("tests/data/test_package_bar.txt", "r").read()
        foo = open("tests/data/test_package_bar_foo.txt", "r").read()
        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children=[
                Class(name = "brabbel", children = [
                    Constructor(symbol="SYM_FIXME"),
                    Variable("field1", Type_Reference(Identifier(["bar", "baz", "my_type"]))),
                    Variable("field2", Type_Reference(Identifier(["local_type"]))),
                    Variable("field3", Type_Reference(Identifier(["bar", "foo", "blub", "some_type"])))]
                    )])]).AdaSpecification()
        self.assertTrue(result[2] == expected, "Invalid class: >>>\n" + result[2] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[1] == foo, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + foo + "\n<<<")
        self.assertTrue(result[0] == bar, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + bar + "\n<<<")

    def test_class_elements_local_types(self):
        expected = open("tests/data/test_class_with_local_types.txt", "r").read()
        bar = open("tests/data/test_package_bar.txt", "r").read()
        foo = open("tests/data/test_package_bar_foo.txt", "r").read()
        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "brabbel", children = [
                    Constructor(symbol="SYM_FIXME"),
                    Variable("field1", Type_Reference(Identifier(["bar", "baz", "my_type"]))),
                    Variable("field2", Type_Reference(Identifier(["local_type"]))),
                    Variable("field3", Type_Reference(Identifier(["bar", "foo", "blub", "some_type"]))),
                    Variable("field4", Type_Reference(Identifier(["bar", "foo", "brabbel", "some_type"]))),
                    ])])]).AdaSpecification()
        self.assertTrue(result[2] == expected, "Invalid class: >>>\n" + result[2] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[1] == foo, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + foo + "\n<<<")
        self.assertTrue(result[0] == bar, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + bar + "\n<<<")

    def test_class_functions_with_return_type(self):
        expected = open("tests/data/test_class_functions_with_return_type.txt", "r").read()
        bar = open("tests/data/test_package_bar.txt", "r").read()
        foo = open("tests/data/test_package_bar_foo.txt", "r").read()
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
        self.assertTrue(result[2] == expected, "Invalid class: >>>\n" + result[2] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[1] == foo, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + foo + "\n<<<")
        self.assertTrue(result[0] == bar, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + bar + "\n<<<")

    def test_constant(self):
        Constant("someconstant", 123).AdaSpecification() == "someconstant : constant := 123"

    def test_namespace_with_constants(self):
        expected = open("tests/data/test_namespace_with_constants.txt", "r").read()
        bar = open("tests/data/test_package_bar.txt", "r").read()
        foo = open("tests/data/test_package_bar_foo.txt", "r").read()
        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Namespace(name = "namespace", children = [
                    Constant(name = "constant1", value = 5),
                    Constant(name = "constant2", value = 42)]
                    )])]).AdaSpecification()
        self.assertTrue(result[2] == expected, "Invalid class: >>>\n" + result[2] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[1] == foo, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + foo + "\n<<<")
        self.assertTrue(result[0] == bar, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + bar + "\n<<<")

    def test_class_with_constants(self):
        expected = open("tests/data/test_class_with_constants.txt", "r").read()
        bar = open("tests/data/test_package_bar.txt", "r").read()
        foo = open("tests/data/test_package_bar_foo.txt", "r").read()
        result = Namespace(name = "bar", children = [
            Namespace(name = "foo", children = [
                Class(name = "class", children = [
                    Constructor(symbol="symbol_404"),
                    Constant(name = "constant1", value = 5),
                    Constant(name = "constant2", value = 42)]
                    )])]).AdaSpecification()
        self.assertTrue(result[2] == expected, "Invalid class: >>>\n" + result[2] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[1] == foo, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + foo + "\n<<<")
        self.assertTrue(result[0] == bar, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + bar + "\n<<<")

    def test_empty_namespace(self):
        expected = open("tests/data/test_empty_namespace.txt", "r").read()
        blah = open("tests/data/test_package_blah.txt", "r").read()
        result = Namespace(name="blah", children=[Namespace(name = "blubb")]).AdaSpecification()
        self.assertTrue(result[1] == expected, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[0] == blah, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + blah + "\n<<<")

    def test_enumeration(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1"),
                                   Constant(name = "elem2")]).AdaSpecification()
        self.assertTrue(result == "type Foo is (Elem1, Elem2)", "Invalid: >>>" + result + "<<<")

    def test_class_with_enum(self):
        expected = open("tests/data/test_class_with_enum.txt", "r").read()
        bar = open("tests/data/test_package_bar.txt", "r").read()
        foo = open("tests/data/test_package_bar_foo.txt", "r").read()
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
        self.assertTrue(result[2] == expected, "Invalid class: >>>\n" + result[2] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[1] == foo, "Invalid package: >>>\n" + result[1] + "\n<<< expected: >>>\n" + foo + "\n<<<")
        self.assertTrue(result[0] == bar, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + bar + "\n<<<")

    def test_enum_representation(self):
        result = Enum(name      = "foo",
                      children  = [Constant(name = "elem1", value = 50),
                                   Constant(name = "elem2", value = 1234)]).AdaRepresentation()
        self.assertTrue(result == "for Foo use (Elem1 => 50, Elem2 => 1234)", "Invalid: >>>" + result + "<<<")

    def test_class_multiple_constructors(self):
        expected = open("tests/data/test_class_multiple_constructors.txt", "r").read()
        foo = open("tests/data/test_package_foo.txt", "r").read()
        result = Namespace(name = "foo", children = [
            Class(name = "brabbel", children = [
                Constructor(symbol = "SYM_FIXME"),
                Constructor(symbol = "SYM_FIXME", parameters = [
                    Variable(name = "arg", ctype = Type_Reference(name=Identifier(["integer"])))])]
                )]).AdaSpecification()
        self.assertTrue(result[1] == expected, "Invalid class: >>>\n" + result[1] + "\n<<< expected: >>>\n" + expected + "\n<<<")
        self.assertTrue(result[0] == foo, "Invalid package: >>>\n" + result[0] + "\n<<< expected: >>>\n" + foo + "\n<<<")
