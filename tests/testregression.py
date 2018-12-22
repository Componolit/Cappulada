import unittest
import clang.cindex
from capdpa import *
from capdpa_test import *

class Regression(Capdpa_Test):

    def test_template_with_class_argument(self):
        unused = CXX("tests/data/test_template_class_argument.h").ToIR(project="Capdpa")

if __name__ == '__main__':
    unittest.main()
