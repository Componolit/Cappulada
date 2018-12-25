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

    def test_class_from_default_constructor(self):
        self.check_validation("test_class_from_default_constructor")

    def test_namespace_with_const_variable(self):
        self.check_validation("test_namespace_with_const_variable")

    def test_project_with_reserved_name(self):
        try:
            Generator("class", "tests/cache/class", ["tests/data/class/impl.cpp"]).run()
            self.fail("Invalid project name \"class\" not detected")
        except generator.InvalidProjectName:
            pass
        except:
            self.fail("Invalid project name \"class\" not detected")

        try:
            Generator("constructor", "tests/cache/class", ["tests/data/class/impl.cpp"]).run()
            self.fail("Invalid project name \"constructor\" not detected")
        except generator.InvalidProjectName:
            pass
        except:
            self.fail("Invalid project name \"constructor\" not detected")

    def test_multiple_members_with_private_type(self):
        self.check_validation("test_multiple_members_with_private_type")

    def test_class_from_custom_constructor(self):
        self.check_validation("test_class_from_custom_constructor")

if __name__ == '__main__':
    unittest.main()
