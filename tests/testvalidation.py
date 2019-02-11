#!/usr/bin/env python

import sys
if __name__ == '__main__':
    sys.path.append (".")

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

        result = call(["gnatprove", "--mode", "check_all", "-q", "-P", "tests/data/testcase.gpr", "-XName=" + name])
        self.assertEqual(result, 0, "Gnatprove failed")

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

    def test_class_with_class_pointer_member(self):
        self.check_validation("test_class_with_class_pointer_member")

    def test_builtin_types(self):
        self.check_validation("test_builtin_types")

    def test_template_instance(self):
        self.check_validation("test_template_instance")

    def test_class_variable(self):
        self.check_validation("test_class_variable")

    def test_void_pointer_member(self):
        self.check_validation("test_void_pointer_member")

    def test_private_void_pointer_member(self):
        self.check_validation("test_private_void_pointer_member")

    def test_class_inheritance_early(self):
        self.check_validation("test_class_inheritance_early")

    def test_class_inheritance_early_overloaded(self):
        self.check_validation("test_class_inheritance_early_overloaded")

    def test_class_inheritance_late(self):
        self.check_validation("test_class_inheritance_late")

    def test_nested_class(self):
        self.check_validation("test_nested_class")

    def test_member_pointer(self):
        self.check_validation("test_member_pointer")

    def test_member_reference(self):
        self.check_validation("test_member_reference")

    def test_enumeration_member(self):
        self.check_validation("test_enumeration_member")

    def test_enumeration_declaration(self):
        self.check_validation("test_enumeration_declaration")

    def test_enumeration_values(self):
        self.check_validation("test_enumeration_values")

    def test_enum_with_excess_value(self):
        self.check_validation("test_enum_with_excess_value")

    def test_export_method(self):
        self.check_validation("test_export_method")

    def test_enumeration_custom_base_type(self):
        self.check_validation("test_enumeration_custom_base_type")

    def test_enumeration_class(self):
        self.check_validation("test_enumeration_class")

    def test_static_class_member(self):
        self.check_validation("test_static_class_member")

    def test_private_static_class_member(self):
        self.check_validation("test_private_static_class_member")

    def test_private_reference_member(self):
        self.check_validation("test_private_reference_member")

    def test_function_pointer(self):
        self.check_validation("test_function_pointer")

    def test_namespace_with_typedefs(self):
        self.check_validation("test_namespace_with_typedefs")

    def test_constant_arrays(self):
        self.check_validation("test_constant_arrays")

    def test_dependent_arrays(self):
        self.check_validation("test_dependent_arrays")

    def test_nested_private_class(self):
        self.check_validation("test_nested_private_class")

if __name__ == '__main__':
    unittest.main()
