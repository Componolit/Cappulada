# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class Mangling(unittest.TestCase):

    def test_class_with_virtual(self):
        c = Class (name     = "With_Virtual",
                   children = [Function(name = "foo",
                                        symbol     = "",
                                        parameters = None)])
        result = c.children[1].Mangle()
        self.assertTrue(result == "_ZN12With_Virtual3fooEv", "Invalid symbol: " + result)

    def test_class_with_functions_void (self):
        c = Class (name     = "With_functions",
                  children  = [Function(name = "public_function",
                                        symbol     = "",
                                        parameters = [Variable (None, Type_Reference(["int"]))])])

        result = c.children[1].Mangle()
        self.assertTrue(result == "_ZN14With_functions15public_functionEi", "Invalid symbol: " + result)

    def test_class_with_functions_int (self):
        c = Class (name     = "With_functions",
                   children = [Function(name        = "named_param",
                                        symbol      = "",
                                        parameters  = [Variable ("param", Type_Reference(["int"]))],
                                        return_type = Type_Reference(["int"]))])

        result = c.children[1].Mangle()
        self.assertTrue(result == "_ZN14With_functions11named_paramEi", "Invalid symbol: " + result)

    def test_class_with_functions_ctor (self):
        c = Class (name     = "With_functions",
                   children = [Constructor(symbol     = "",
                                           parameters = None)])
        result = c.children[0].Mangle()
        self.assertTrue(result == "_ZN14With_functionsC1Ev", "Invalid symbol: " + result)

    # FIXME: Missing
    #   * Templates
    #   * Functions with non-primitive argument types
    #   * Functions with pointer argument types
