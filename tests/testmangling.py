# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class Mangling(unittest.TestCase):

    def test_const_outside_namespace(self):
        result = Constructor(symbol     = "",
                             parameters = None).Mangle()
        self.assertTrue(result == "_ZN3foo3barC1Ev", "Invalid constant: " + result)

    def test_class_with_virtual(self):
        result = Function(name = Identifier(["With_Virtual", "foo"]),
                          symbol     = "",
                          parameters = None).Mangle()
        self.assertTrue(result == "_ZN12With_Virtual3fooEv", "Invalid symbol: " + result)

    def test_class_with_functions_void (self):
        result = Function(name = Identifier(["With_functions", "public_function"]),
                          symbol     = "",
                          parameters = [Variable (None, Type_Reference(["int"]))]).Mangle()
        self.assertTrue(result == "_ZN14With_functions15public_functionEi", "Invalid symbol: " + result)

    def test_class_with_functions_int (self):
        result = Function(name = Identifier(["With_functions", "named_param"]),
                          symbol      = "",
                          parameters  = [Variable ("param", Type_Reference(["int"]))],
                          return_type = Type_Reference(["int"])).Mangle()
        self.assertTrue(result == "_ZN14With_functions11named_paramEi", "Invalid symbol: " + result)

    def test_class_with_functions_ctor (self):
        c = Class (name     = "With_function",
                   children = [Constructor(symbol     = "",
                                           parameters = None)])
        result = c.children[0].Mangle()
        self.assertTrue(result == "_ZN14With_functionsC1Ev", "Invalid symbol: " + result)
