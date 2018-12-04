# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class Mangling(unittest.TestCase):

    def setUp(self):
        self.templates   = CXX("tests/data/test_template_mangling.h").ToIR(project="Capdpa").children
        self.compression = CXX("tests/data/mangling_compression.h").ToIR(project="Capdpa").children

    def test_class_with_virtual(self):
        c = Class (name     = "With_Virtual",
                   children = [Function(name = "foo",
                                        symbol     = "",
                                        parameters = None)])
        result = c.children[1].Mangle("Capdpa")
        self.assertTrue(result == "_ZN12With_Virtual3fooEv", "Invalid symbol: " + result)

    def test_class_with_functions_void (self):
        c = Class (name     = "With_functions",
                  children  = [Function(name = "public_function",
                                        symbol     = "",
                                        parameters = [Variable (None, Type_Reference(name=Identifier(["Capdpa", "int"])))])])

        result = c.children[1].Mangle("Capdpa")
        self.assertTrue(result == "_ZN14With_functions15public_functionEi", "Invalid symbol: " + result)

    def test_class_with_functions_int (self):
        c = Class (name     = "With_functions",
                   children = [Function(name        = "named_param",
                                        symbol      = "",
                                        parameters  = [Variable (Identifier(name=["Capdpa", "param"]), Type_Reference(name=Identifier(["Capdpa", "int"])))],
                                        return_type = Type_Reference(["int"]))])

        result = c.children[1].Mangle("Capdpa")
        self.assertTrue(result == "_ZN14With_functions11named_paramEi", "Invalid symbol: " + result)

    def test_class_with_functions_ctor (self):
        c = Class (name     = "With_functions",
                   children = [Constructor(symbol     = "",
                                           parameters = None)])
        result = c.children[0].Mangle("Capdpa")
        self.assertTrue(result == "_ZN14With_functionsC1Ev", "Invalid symbol: " + result)

    def test_template_template_argument (self):
        symbol = self.templates[2].children[1].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN6Capdpa3Cls3barE6Capdpa5TemplIciEc", "Invalid symbol: " + symbol)

    def test_template_no_template_argument (self):
        symbol = self.templates[2].children[2].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN6Capdpa3Cls3fooEic", "Invalid symbol: " + symbol)

    def test_template_multiple_template_arguments (self):
        symbol = self.templates[2].children[3].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN6Capdpa3Cls3bazE6Capdpa5TemplIciES0_IccE", "Invalid symbol: " + symbol)

    def xtest_template_4 (self):
        symbol = self.templates[0].children[1].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN6Capdpa3Cls3varE6Capdpa3VarIJEEc", "Invalid symbol: " + symbol)

    def test_compression_none (self):
        symbol = self.compression[0].children[1].children[1].Mangle("Capdpa")
        self.assertTrue (symbol == "foo", "Invalid symbol: " + symbol)

    # FIXME: Missing
    #   * Templates
    #   * Functions with non-primitive argument types
    #   * Functions with pointer argument types
