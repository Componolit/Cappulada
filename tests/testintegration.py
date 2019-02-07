#!/usr/bin/env python

import sys
if __name__ == '__main__':
    sys.path.append (".")

import os
import unittest
from capdpa import *
from capdpa_test import *

class check_integration(Capdpa_Test):

    def check_integration(self, header, specs):
        hname = os.path.splitext(header)[0]
        result = CXX("tests/data/integration/" + header).ToIR(project=hname).AdaSpecification()
        self.assertEqual(len(specs), len(result), "Expected {} compilation units, got {}\n====\n{}"
                .format(len(specs), len(result), result))
        result = [r.Text() for r in result]
        map(lambda r, s: self.cache (r, s, directory = "integration"), result, specs)
        map(self.check, result, map(lambda s: self.load (s, "integration"), specs))

    def test_empty_namespace(self):
        self.check_integration(
                "test_empty_namespace.h", [
                    "test_empty_namespace.ads",
                    "test_empty_namespace-empty.ads"])

    def test_namespace_with_constants(self):
        self.check_integration(
                "test_namespace_with_constants.h", [
                    "test_namespace_with_constants.ads",
                    "test_namespace_with_constants-with_constants.ads"])

    def test_empty_class(self):
        self.check_integration(
                "test_empty_class.h", ["test_empty_class.ads"])

    def test_namespace_with_class(self):
        self.check_integration(
                "test_namespace_with_class.h", [
                    "test_namespace_with_class.ads",
                    "test_namespace_with_class-with_class.ads"])

    def test_namespace_with_enum(self):
        self.check_integration(
                "test_namespace_with_enum.h", [
                    "test_namespace_with_enum.ads",
                    "test_namespace_with_enum-with_enum.ads"])

    def test_class_with_constants(self):
        self.check_integration(
                "test_class_with_constants.h", ["test_class_with_constants.ads"])

    def test_class_with_members(self):
        self.check_integration(
                "test_class_with_members.h", ["test_class_with_members.ads"])

    def test_class_with_functions(self):
        self.check_integration(
                "test_class_with_functions.h", ["test_class_with_functions.ads"])

    def test_namespace_with_class_with_everything(self):
        self.check_integration("test_namespace_with_class_with_everything.h", [
            "test_namespace_with_class_with_everything.ads",
            "test_namespace_with_class_with_everything-with_class.ads"])

    def EXCLUDE_test_class_with_class_type(self):
        self.check_integration("test_class_with_class_type.h", [
            "test_class_with_class_type.ads",
            "test_class_with_class_type-with_class.ads"])

    def test_types(self):
        self.check_integration("test_types.h", ["test_types.ads"])

    def test_namespace_with_typedef(self):
        self.check_integration("test_namespace_with_typedef.h", [
            "test_namespace_with_typedef.ads",
            "test_namespace_with_typedef-with_typedef.ads"])

    def test_namespace_with_typedef_with_class(self):
        self.check_integration("test_namespace_with_typedef_with_class.h", [
             "test_namespace_with_typedef_with_class.ads",
             "test_namespace_with_typedef_with_class-with_typedef.ads"])

    def test_with_template(self):
        self.check_integration("test_with_template.h", ["test_with_template.ads"])

    def test_base_with_virtual(self):
        self.check_integration("test_base_with_virtual.h", ["test_base_with_virtual.ads"])

    def test_class_inheritace(self):
        self.check_integration("test_class_inheritance.h", ["test_class_inheritance.ads"])

    def test_inherit_from_virtual(self):
        self.check_integration("test_inherit_from_virtual.h", ["test_inherit_from_virtual.ads"])

    def test_child_class(self):
        self.check_integration("test_child_class.h", ["test_child_class.ads"])

    def test_inherit_virtual_from_simple(self):
        self.check_integration("test_inherit_virtual_from_simple.h", ["test_inherit_virtual_from_simple.ads"])

    def test_nested_class(self):
        self.check_integration("test_nested_class.h", ["test_nested_class.ads"])

    def test_pointer_member(self):
        self.check_integration("test_pointer_member.h", ["test_pointer_member.ads"])

    def test_reference_member(self):
        self.check_integration("test_reference_member.h", ["test_reference_member.ads"])

    def test_enum_member(self):
        self.check_integration("test_enum_member.h", ["test_enum_member.ads"])

    def test_class_with_array(self):
        self.check_integration("test_class_with_arrays.h", [
            "test_class_with_arrays.ads"])

    def test_class_with_struct_type(self):
        self.check_integration("test_class_with_struct_type.h", ["test_class_with_struct_type.ads"])

    def test_class_with_static_functions(self):
        self.check_integration(
                "test_class_with_static_functions.h", ["test_class_with_static_functions.ads"])

    def EXCLUDE_test_class_with_namespace_members(self):
        self.check_integration(
                "test_class_with_namespace_members.h",
                ["test_class_with_namespace_members.ads",
                 "test_class_with_namespace_members-foo.ads",
                 "test_class_with_namespace_members-root.ads"])

if __name__ == '__main__':
    unittest.main()
