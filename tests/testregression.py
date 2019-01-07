#!/usr/bin/env python

import unittest
import clang.cindex
from capdpa import *
from capdpa_test import *

class Regression(Capdpa_Test):

    def EXCLUDE_test_template_with_class_argument(self):
        unused = CXX("tests/data/test_template_class_argument.h").ToIR(project="Capdpa")

    def test_external_method_def(self):
        unused = CXX("tests/data/test_external_method_def.cpp").ToIR(project="Capdpa").AdaSpecification()

    def test_private_constructor(self):
        unused = CXX("tests/data/test_private_constructor.h").ToIR(project="Capdpa").AdaSpecification()

if __name__ == '__main__':
    unittest.main()
