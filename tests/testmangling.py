# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class Mangling(unittest.TestCase):

    def test_const_outside_namespace(self):
        result = Mangle(Function(name       = Identifier(["foo", "bar"]),
                                 symbol     = "",
                                 parameters = None)).ToString()
        self.assertTrue(result == "_ZN3foo3barC1Ev", "Invalid constant: " + result)
