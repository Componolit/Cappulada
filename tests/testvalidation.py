import unittest

from subprocess import call
from capdpa_test import *
from capdpa import *

class check_validation(Capdpa_Test):

    def check_integration(self, name):

        Generator(project = name + "_ada",
                  outdir  = "tests/cache",
                  headers = ["tests/data/" + name + ".cpp"]).run()

        result = call(["gprbuild", "-q", "-P", "tests/data/testcase.gpr", "-XMain=" + name + "_main.adb"])
        self.assertEqual(result, 0, "Build failed")

        result = call(["tests/cache/" + name + "_main"])
        self.assertEqual(result, 0, "Running test case failed")

    def test_namespace_with_const_variable(self):
        result = self.check_integration("test_namespace_with_const_variable")

if __name__ == '__main__':
    unittest.main()
