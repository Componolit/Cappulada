# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class GenerateConstant(unittest.TestCase):

    def test_simple_constant(self):
        result = Constant("whats_the_question", 42).AdaSpecification()
        self.assertTrue(result == "Whats_The_Question : constant := 42;",
                        "Invalid constant: " + result);

    def test_simple_negative_constant(self):
        result = Constant("negative", -42).AdaSpecification()
        self.assertTrue(result == "Negative : constant := -42;",
                        "Invalid constant: " + result);

    def test_identifier_escape_begin(self):
        result = Constant("_invalid").AdaSpecification()
        self.assertTrue(result == "X_Invalid : constant := 0;",
                        "Invalid constant: " + result);

    def test_identifier_escape_begin_digit(self):
        result = Constant("42invalid").AdaSpecification()
        self.assertTrue(result == "X42invalid : constant := 0;",
                        "Invalid constant: " + result);

    def test_identifier_escape_end(self):
        result = Constant("invalid_").AdaSpecification()
        self.assertTrue(result == "Invalid_X : constant := 0;",
                        "Invalid constant: " + result);

    def test_identifier_double_underscore(self):
        result = Constant("inv__alid").AdaSpecification()
        self.assertTrue(result == "Inv_X_Alid : constant := 0;",
                        "Invalid constant: " + result);

    def test_identifier_multiple_underscores(self):
        result = Constant("inv____alid").AdaSpecification()
        self.assertTrue(result == "Inv_X_X_X_Alid : constant := 0;",
                        "Invalid constant: " + result);

    def test_identifier_reserved_word1(self):
        result = Constant("begin").AdaSpecification()
        self.assertTrue(result == "X_Begin : constant := 0;",
                        "Invalid constant: " + result);

    def test_identifier_reserved_word2(self):
        result = Constant("while").AdaSpecification()
        self.assertTrue(result == "X_While : constant := 0;",
                        "Invalid constant: " + result);

    def test_unsupported_character(self):
        result = Constant("Thüringer_Klöße").AdaSpecification()
        self.assertTrue(result == "Thc3bcringer_Klc3b6c39fe : constant := 0;",
                        "Invalid constant: " + result);

    def test_class_simple(self):
        expected = open("tests/data/test_class_simple.txt", "r").read()
        result = Class(["foo", "brabbel"], constructor=Function(name="brabbel", symbol="SYM_FIXME")).AdaSpecification();
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<");

    def test_class_elements(self):
        expected = open("tests/data/test_class_with_elements.txt", "r").read()
        result = Class(["bar", "foo", "brabbel"],
                       constructor=Function(name="brabbel", symbol="SYM_FIXME"),
                       members=[Variable("field1", Type(["int"], 4)), Variable("field2", Type(["long"], 8))]).AdaSpecification();
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<");

    def test_class_elements_external_types(self):
        expected = open("tests/data/test_class_with_external_types.txt", "r").read()
        result = Class(["bar", "foo", "brabbel"],
                       constructor=Function(name="brabbel", symbol="SYM_FIXME"),
                       members=[Variable("field1", Type(["bar", "baz", "my_type"], 40, False)),
                                Variable("field2", Type(["local_type"], 16)),
                                Variable("field3", Type(["bar", "foo", "blub", "some_type"], 100, False))]).AdaSpecification();
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<");

    def test_class_elements_local_types(self):
        expected = open("tests/data/test_class_with_local_types.txt", "r").read()
        result = Class(["bar", "foo", "brabbel"],
                       constructor=Function(name="brabbel", symbol="SYM_FIXME"),
                       members=[Variable("field1", Type(["bar", "baz", "my_type"], 40, False)),
                                Variable("field2", Type(["local_type"], 16)),
                                Variable("field3", Type(["bar", "foo", "blub", "some_type"], 4)),
                                Variable("field4", Type(["bar", "foo", "brabbel", "some_type"], 100, False)),
                        ]).AdaSpecification();
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<");

    def test_class_functions_with_return_type(self):
        expected = open("tests/data/test_class_functions_with_return_type.txt", "r").read()
        result = Class(name         = ["bar", "foo", "brabbel"],
                       constructor  = Function(name="brabbel", symbol="SYM_FIXME"),
                       members      = [Variable("field1", Type(["bar", "baz", "my_type"], 8)),
                                       Variable("field2", Type(["local_type"], 24, False)),
                                       Variable("field3", Type(["bar", "foo", "blub", "some_type"], 12))],
                       functions    = [Function(name        = ["bar", "foo", "brabbel", "do_something"],
                                                symbol      = "this_function_has_a_funny_symbol",
                                                parameters  = [Variable("param1", Type(["foo", "bar"], 20, False)),
                                                               Variable("param2", Type(["foo", "baz"], 10))],
                                                return_type = Type(["Blah", "Some_Type"], 10))]
                      ).AdaSpecification();
        self.assertTrue(result == expected, "Invalid class: >>>" + result + "<<< expected: >>>" + expected + "<<<");
