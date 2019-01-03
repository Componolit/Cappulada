import unittest

from subprocess import call
from capdpa_test import *
from capdpa import *

class check_validation(Capdpa_Test):

    @classmethod
    def setUpClass(self):
        if not os.path.exists("tests/compile/"):
            os.mkdir("tests/compile/")

    def check_validation(self, name):

        Generator(project = name,
                  outdir  = "tests/compile/" + name,
                  headers = ["tests/data/" + name + "/impl.h"]).run()

        result = call(["gprbuild", "-q", "-P", "tests/data/testcase.gpr", "-XName=" + name])
        self.assertEqual(result, 0, "Build failed")

        result = call(["tests/compile/" + name + "/main"])
        self.assertEqual(result, 0, "Running test case failed")

    def test_class_from_default_constructor(self):
        self.check_validation("test_class_from_default_constructor")

    def test_namespace_with_const_variable(self):
        self.check_validation("test_namespace_with_const_variable")

    def test_project_with_reserved_name(self):
        try:
            Generator("class", "tests/compile/class", ["tests/data/class/impl.cpp"]).run()
            self.fail("Invalid project name \"class\" not detected")
        except generator.InvalidProjectName:
            pass
        except:
            self.fail("Invalid project name \"class\" not detected")

        try:
            Generator("constructor", "tests/compile/class", ["tests/data/class/impl.cpp"]).run()
            self.fail("Invalid project name \"constructor\" not detected")
        except generator.InvalidProjectName:
            pass
        except:
            self.fail("Invalid project name \"constructor\" not detected")

    def test_multiple_members_with_private_type(self):
        self.check_validation("test_multiple_members_with_private_type")

    def test_class_from_custom_constructor(self):
        self.check_validation("test_class_from_custom_constructor")

    def test_multiple_custom_constructors(self):
        self.check_validation("test_multiple_custom_constructors")

    def test_namespace_with_class(self):
        self.check_validation("test_namespace_with_class")

    def test_complex_class_layout(self):
        self.check_validation("test_complex_class_layout")

    def test_namespace_with_enumeration(self):
        self.check_validation("test_namespace_with_enumeration")

    def test_namespace_with_constants(self):
        self.check_validation("test_namespace_with_constants")

    def test_namespace_with_functions(self):
        self.check_validation("test_namespace_with_functions")

    def test_function_outside_namespace(self):
        self.check_validation("test_function_outside_namespace")

    def test_static_method(self):
        self.check_validation("test_static_method")

    def test_static_parameterless(self):
        self.check_validation("test_static_parameterless")

    def test_class_with_constants(self):
        self.check_validation("test_class_with_constants")

    def test_class_members(self):
        self.check_validation("test_class_members")

    def test_class_methods(self):
        self.check_validation("test_class_methods")

    def test_class_with_class_type_member(self):
        self.check_validation("test_class_with_class_type_member")

if __name__ == '__main__':
    unittest.main()
