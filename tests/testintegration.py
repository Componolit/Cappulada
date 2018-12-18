
import unittest
from capdpa import *
from capdpa_test import *

class check_integration(Capdpa_Test):

    def check_integration(self, header, specs):
        result = CXX("tests/data/" + header).ToIR(project="Capdpa").AdaSpecification()
        self.assertEqual(len(specs), len(result), "Expected {} compilation units, got {}\n====\n{}"
                .format(len(specs), len(result), result))
        result = [r.Text() for r in result]
        map(self.cache, result, specs)
        map(self.check, result, map(self.load, specs))

    def test_empty_namespace(self):
        self.check_integration(
                "test_empty_namespace.h", [
                    "test_capdpa.ads",
                    "test_empty_namespace.ads"])

    def test_namespace_with_constants(self):
        self.check_integration(
                "test_namespace_with_constants.h", [
                    "test_capdpa.ads",
                    "test_namespace_with_constants.ads"])

    def test_empty_class(self):
        self.check_integration(
                "test_empty_class.h", [
                    "test_capdpa.ads",
                    "test_empty_class.ads"])

    def test_namespace_with_class(self):
        self.check_integration(
                "test_namespace_with_class.h",[
                    "test_capdpa.ads",
                    "test_namespace_with_class.ads",
                    "test_class_in_namespace.ads"])

    def test_namespace_with_enum(self):
        self.check_integration(
                "test_namespace_with_enum.h", [
                    "test_capdpa.ads",
                    "test_namespace_with_enum.ads"])

    def test_class_with_constants(self):
        self.check_integration(
                "test_class_with_constants.h", [
                    "test_capdpa.ads",
                    "test_class_with_constants.ads"])

    def test_class_with_members(self):
        self.check_integration(
                "test_class_with_members.h", [
                    "test_capdpa.ads",
                    "test_class_with_members.ads"])

    def test_class_with_functions(self):
        self.check_integration(
                "test_class_with_functions.h", [
                    "test_capdpa.ads",
                    "test_class_with_functions.ads"])

    def test_namespace_with_class_with_everything(self):
        self.check_integration("test_namespace_with_class_with_everything.h", [
            "test_capdpa.ads",
            "test_namespace_with_class.ads",
            "test_namespace_with_class_with_everything.ads"])

    def test_class_with_class_type(self):
        self.check_integration("test_class_with_class_type.h", [
            "test_capdpa.ads",
            "test_namespace_with_class.ads",
            "test_class_in_namespace.ads",
            "test_class_with_class_type.ads"])

    def test_types(self):
        self.check_integration("test_types.h", [
            "test_capdpa_with_types.ads"])

    def test_namespace_with_typedef(self):
        self.check_integration("test_namespace_with_typedef.h", [
            "test_capdpa.ads",
            "test_namespace_with_typedef.ads"])

    def test_namespace_with_typedef_with_class(self):
        self.check_integration("test_namespace_with_typedef_with_class.h", [
            "test_capdpa.ads",
            "test_namespace_with_typedef.ads",
            "test_namespace_with_typedef_with_class.ads"])

    def test_with_template(self):
        self.check_integration("test_with_template.h", [
            "test_capdpa.ads",
            "test_template_int_char.ads",
            "test_template_int_int.ads",
            "test_template_user.ads"])

    def test_class_with_virtual(self):
        self.check_integration("test_base_with_virtual.h", [
            "test_capdpa.ads",
            "test_base_with_virtual.ads"])

    def test_simple_inheritace(self):
        self.check_integration("test_class_inheritance.h", [
            "test_capdpa.ads",
            "test_class_with_members.ads",
            "test_class_inheritance.ads"])

    def test_inheritance_from_virtual(self):
        self.check_integration("test_inherit_from_virtual.h", [
            "test_capdpa.ads",
            "test_base_with_virtual.ads",
            "test_inherit_from_virtual.ads"])

    def test_simple_inheritance_chain(self):
        self.check_integration("test_child_class.h", [
            "test_capdpa.ads",
            "test_class_with_members.ads",
            "test_class_inheritance.ads",
            "test_child_class.ads"])

    def test_virtual_from_simple(self):
        self.check_integration("test_inherit_virtual_from_simple.h", [
            "test_capdpa.ads",
            "test_class_with_members.ads",
            "test_class_inheritance.ads",
            "test_inherit_virtual_from_simple.ads"])

    def test_nested_class(self):
        self.check_integration("test_nested_class.h", [
            "test_capdpa.ads",
            "test_nested_package.ads"])

    def test_pointer_member(self):
        self.check_integration("test_pointer_member.h", [
            "test_capdpa.ads",
            "test_pointer_member.ads"])

    def test_reference_member(self):
        self.check_integration("test_reference_member.h", [
            "test_capdpa.ads",
            "test_reference_member.ads"])

    def test_enum_member(self):
        self.check_integration("test_enum_member.h", [
            "test_capdpa.ads",
            "test_enum_member.ads"])

    def test_class_with_array(self):
        self.check_integration("test_class_with_array.h", [
            "test_capdpa.ads",
            "test_class_with_array.ads"])

    def test_class_with_struct_type(self):
        self.check_integration("test_class_with_struct_type.h", [
            "test_capdpa.ads",
            "test_class_with_struct_type.ads"])

    def test_class_with_static_functions(self):
        self.check_integration(
                "test_class_with_static_functions.h", [
                    "test_capdpa.ads",
                    "test_class_with_static_functions.ads"])

if __name__ == '__main__':
    unittest.main()
