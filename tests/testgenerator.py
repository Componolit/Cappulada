import unittest
from capdpa import *

class GenerateConstant(unittest.TestCase):
    
    def test_simple_constant(self):
        self.assertTrue(Constant("whats_the_question", 42).AdaSpecification() ==
            "whats_the_question : constant := 42;", "Invalid constant");

    def test_simple_negative_constant(self):
        self.assertTrue(Constant("negative", -42).AdaSpecification() ==
            "negative : constant := -42;", "Invalid constant");

