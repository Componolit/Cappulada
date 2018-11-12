
import os
import unittest
from capdpa import *

class Capdpa_Test(unittest.TestCase):


    def check(self, a, b):
        return self.assertEqual(a, b, "Invalid entity: >>>\n" + str(a) + "\n<<< expected: >>>\n" + str(b) + "\n<<<")

    def load(self, spec):
        return open("tests/data/" + spec, "r").read()

    def cache(self, res, spec):
        if not os.path.exists("tests/cache/"):
            os.mkdir("tests/cache/")
        return open("tests/cache/" + spec, "w").write(res)

