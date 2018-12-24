import unittest

from subprocess import call
from capdpa_test import *
from capdpa import *

class check_validation(Capdpa_Test):

    def check_validation(self, name):

        Generator(project = name,
                  outdir  = "tests/cache/" + name,
                  headers = ["tests/data/" + name + "/impl.cpp"]).run()

        result = call(["gprbuild", "-q", "-P", "tests/data/testcase.gpr", "-XName=" + name])
        self.assertEqual(result, 0, "Build failed")

        result = call(["tests/cache/" + name + "/main"])
        self.assertEqual(result, 0, "Running test case failed")

    def test_namespace_with_const_variable(self):
        result = self.check_validation("test_namespace_with_const_variable")

if __name__ == '__main__':
    unittest.main()
