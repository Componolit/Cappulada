
import os
import unittest
import difflib
from capdpa import *

class Capdpa_Test(unittest.TestCase):

    def check(self, a, b):
        return self.assertEqual(a, b,
            "Invalid entity:\n " + " ".join(difflib.unified_diff(str(a).splitlines(1), str(b).splitlines(1), "Expected", "Result")))

    def load(self, spec, directory=""):
        return open("tests/data/" + directory + "/" + spec, "r").read()

    def cache(self, res, spec, directory=""):
        if not os.path.exists("tests/cache/" + directory):
            os.mkdir("tests/cache/" + directory)
        return open("tests/cache/" + directory + "/" + spec, "w").write(res)

