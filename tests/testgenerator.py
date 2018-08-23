# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class GenerateConstant(unittest.TestCase):

    def test_simple_constant(self):
        result = Constant(Identifier(["whats_the_question"]), 42).AdaSpecification()
        self.assertTrue(result == "Whats_The_Question : constant := 42;",
                        "Invalid constant: " + result)

    def test_simple_negative_constant(self):
        result = Constant(Identifier(["negative"]), -42).AdaSpecification()
        self.assertTrue(result == "Negative : constant := -42;",
                        "Invalid constant: " + result)

    def test_identifier_escape_begin(self):
        result = Constant(Identifier(["_invalid"]), 0).AdaSpecification()
        self.assertTrue(result == "X_Invalid : constant := 0;",
                        "Invalid constant: " + result)

    def test_identifier_escape_begin_digit(self):
        result = Constant(Identifier(["42invalid"]), 0).AdaSpecification()
        self.assertTrue(result == "X42invalid : constant := 0;",
                        "Invalid constant: " + result)

    def test_identifier_escape_end(self):
        result = Constant(Identifier(["invalid_"]), 0).AdaSpecification()
        self.assertTrue(result == "Invalid_X : constant := 0;",
                        "Invalid constant: " + result)

    def test_identifier_double_underscore(self):
        result = Constant(Identifier(["inv__alid"]), 0).AdaSpecification()
        self.assertTrue(result == "Inv_X_Alid : constant := 0;",
                        "Invalid constant: " + result)

    def test_identifier_multiple_underscores(self):
        result = Constant(Identifier(["inv____alid"]), 0).AdaSpecification()
        self.assertTrue(result == "Inv_X_X_X_Alid : constant := 0;",
                        "Invalid constant: " + result)

    def test_identifier_reserved_word1(self):
        result = Constant(Identifier(["begin"]), 0).AdaSpecification()
        self.assertTrue(result == "X_Begin : constant := 0;",
                        "Invalid constant: " + result)

    def test_identifier_reserved_word2(self):
        result = Constant(Identifier(["while"]), 0).AdaSpecification()
        self.assertTrue(result == "X_While : constant := 0;",
                        "Invalid constant: " + result)

    def test_unsupported_character(self):
        result = Constant(Identifier(["Thüringer_Klöße"]), 0).AdaSpecification()
        self.assertTrue(result == "Thc3bcringer_Klc3b6c39fe : constant := 0;",
                        "Invalid constant: " + result)

    def test_class_simple(self):
        expected = open("tests/data/test_class_simple.txt", "r").read()
        result = Class(name        = Identifier(["foo", "brabbel"]),
                       constructor = Function(name   = Identifier(["brabbel"]),
                                              symbol = "SYM_FIXME")
                      ).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_class_elements(self):
        expected = open("tests/data/test_class_with_elements.txt", "r").read()
        result = Class(name        = Identifier(["bar", "foo", "brabbel"]),
                       constructor = Function(name   = Identifier(["brabbel"]),
                                              symbol = "SYM_FIXME"),
                       members     = [Variable(Identifier(["field1"]), Type(Identifier(["int"]), 4)),
                                     Variable(Identifier(["field2"]), Type(Identifier(["long"]), 8))]
                      ).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_class_elements_external_types(self):
        expected = open("tests/data/test_class_with_external_types.txt", "r").read()
        result = Class(name        = Identifier(["bar", "foo", "brabbel"]),
                       constructor = Function(name = Identifier(["brabbel"]), symbol="SYM_FIXME"),
                       members     = [Variable(Identifier(["field1"]), Type(Identifier(["bar", "baz", "my_type"]), 40, False)),
                                      Variable(Identifier(["field2"]), Type(Identifier(["local_type"]), 16)),
                                      Variable(Identifier(["field3"]), Type(Identifier(["bar", "foo", "blub", "some_type"]), 100, False))]
                      ).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_class_elements_local_types(self):
        expected = open("tests/data/test_class_with_local_types.txt", "r").read()
        result = Class(name        = Identifier(["bar", "foo", "brabbel"]),
                       constructor = Function(name=Identifier(["brabbel"]), symbol="SYM_FIXME"),
                       members     = [Variable(Identifier(["field1"]), Type(Identifier(["bar", "baz", "my_type"]), 40, False)),
                                      Variable(Identifier(["field2"]), Type(Identifier(["local_type"]), 16)),
                                      Variable(Identifier(["field3"]), Type(Identifier(["bar", "foo", "blub", "some_type"]), 4)),
                                      Variable(Identifier(["field4"]), Type(Identifier(["bar", "foo", "brabbel", "some_type"]), 100, False)),
                        ]).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_class_functions_with_return_type(self):
        expected = open("tests/data/test_class_functions_with_return_type.txt", "r").read()
        result = Class(name         = Identifier(["bar", "foo", "brabbel"]),
                       constructor  = Function(Identifier(["brabbel"]), symbol="SYM_FIXME"),
                       members      = [Variable(Identifier(["field1"]), Type(Identifier(["bar", "baz", "my_type"]), 8)),
                                       Variable(Identifier(["field2"]), Type(Identifier(["local_type"]), 24, False)),
                                       Variable(Identifier(["field3"]), Type(Identifier(["bar", "foo", "blub", "some_type"]), 12))],
                       functions    = [Function(name        = Identifier(["bar", "foo", "brabbel", "do_something"]),
                                                symbol      = "this_function_has_a_funny_symbol",
                                                parameters  = [Variable(Identifier(["param1"]), Type(Identifier(["foo", "bar"]), 20, False)),
                                                               Variable(Identifier(["param2"]), Type(Identifier(["foo", "baz"]), 10))],
                                                return_type = Type(Identifier(["Blah", "Some_Type"]), 10))]
                      ).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_constant(self):
        Constant(Identifier(["someconstant"]), 123).AdaSpecification() == "someconstant : constant := 123"

    def test_namespace_with_constants(self):
        expected = open("tests/data/test_namespace_with_constants.txt", "r").read()
        result = Namespace(name      = Identifier(["bar", "foo", "namespace"]),
                           constants = [Constant(name = Identifier(["constant1"]), value = 5),
                                        Constant(name = Identifier(["constant2"]), value = 42)]
                          ).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_class_with_constants(self):
        expected = open("tests/data/test_class_with_constants.txt", "r").read()
        result = Class(name        = Identifier(["bar", "foo", "class"]),
                       constructor = Function(Identifier(["create_me"]), symbol="symbol_404"),
                       constants   = [Constant(name = Identifier(["constant1"]), value = 5),
                                      Constant(name = Identifier(["constant2"]), value = 42)]
                      ).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_empty_namespace(self):
        expected = open("tests/data/test_empty_namespace.txt", "r").read()
        result = Namespace(name = Identifier(["blah", "blubb"])).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")

    def test_enumeration(self):
        result = Enum(name      = Identifier(["foo"]),
                      constants = [Constant(name = Identifier(["some", "elem1"])),
                                   Constant(name = Identifier(["some", "elem2"]))]).AdaSpecification()
        self.assertTrue(result == "type Foo is (Elem1, Elem2)", "Invalid: >>>" + result + "<<<")

    def test_invalid_enum(self):
        with self.assertRaises(Exception) as context:
            result = Enum(name      = Identifier(["Foo"]),
                          constants = [Constant(name = Identifier(["some", "elem1"]), value = 42)])
        self.assertIn("Element Elem1 of enum Foo must not have a value", context.exception)

    def test_class_with_enum(self):
        expected = open("tests/data/test_class_with_enum.txt", "r").read()
        result = Class(name        = Identifier(["bar", "foo", "class"]),
                       constructor = Function(Identifier(["create_me"]), symbol="symbol_404"),
                       enums       = [Enum(name = Identifier(["enum1"]), constants = [Constant(Identifier(["Elem11"])),
                                                                                      Constant(Identifier(["Elem12"]))]),
                                      Enum(name = Identifier(["enum2"]), constants = [Constant(Identifier(["Elem21"])),
                                                                                      Constant(Identifier(["Elem22"])),
                                                                                      Constant(Identifier(["Elem23"]))])]).AdaSpecification()
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<")
