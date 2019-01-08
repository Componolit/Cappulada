
import os
import unittest
import difflib
from capdpa import *

class Capdpa_Test(unittest.TestCase):

    def check(self, a, b):
        return self.assertEqual(a, b,
            "Invalid entity:\n " + " ".join(difflib.unified_diff(a.splitlines(1), b.splitlines(1), "Expected", "Result")))

    def load(self, spec):
        return open("tests/data/" + spec, "r").read()

    def cache(self, res, spec):
        if not os.path.exists("tests/cache/"):
            os.mkdir("tests/cache/")
        return open("tests/cache/" + spec, "w").write(res)

