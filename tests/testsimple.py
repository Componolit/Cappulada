
import unittest
from capdpa import convert_header

class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_1(self):
        print(convert_header("tests/simple/parser/number.h", ""))

    def test_2(self):
        print(convert_header("tests/simple/parser/number.cc", ""))
