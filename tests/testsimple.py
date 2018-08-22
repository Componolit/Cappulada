
import unittest
from capdpa import convert_header

class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def Xtest_1(self):
        print(convert_header("tests/simple/parser/number.h", ""))

    def Xtest_2(self):
        print(convert_header("tests/simple/parser/number.cc", ""))
