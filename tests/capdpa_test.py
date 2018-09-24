
import unittest
from capdpa import *

class Capdpa_Test(unittest.TestCase):


    check = lambda self, a, b: self.assertEqual(a, b, "Invalid entity: >>>\n" + str(a) + "\n<<< expected: >>>\n" + str(b) + "\n<<<")
    load = lambda self, spec: open("tests/data/" + spec, "r").read()
    cache = lambda self, res, spec: open("tests/cache/" + spec, "w").write(res)

