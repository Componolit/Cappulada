
import unittest
from capdpa import *
from capdpa_test import *

class check_integration(Capdpa_Test):

    def test_empty_namespace(self):
        self.check_integration(
                "test_empty_namespace.h", ["test_empty_namespace.ads"])

    def test_namespace_with_constants(self):
        self.check_integration(
                "test_namespace_with_constants.h",
                ["test_namespace_with_constants.ads"])

    def test_empty_class(self):
        self.check_integration(
                "test_empty_class.h",
                ["test_empty_class.ads"])

    def test_namespace_with_class(self):
        self.check_integration(
                "test_namespace_with_class.h",[
                    "test_namespace_with_class.ads",
                    "test_class_in_namespace.ads"])

    def test_namespace_with_enum(self):
        self.check_integration(
                "test_namespace_with_enum.h",
                ["test_namespace_with_enum.ads"])

    def test_class_with_constants(self):
        self.check_integration(
                "test_class_with_constants.h",
                ["test_class_with_constants.ads"])

    def test_class_with_members(self):
        self.check_integration(
                "test_class_with_members.h",
                ["test_class_with_members.ads"])

    def test_class_with_functions(self):
        self.check_integration(
                "test_class_with_functions.h",
                ["test_class_with_functions.ads"])

    def test_namespace_with_class_with_everything(self):
        self.check_integration("test_namespace_with_class_with_everything.h", [
            "test_namespace_with_class.ads",
            "test_namespace_with_class_with_everything.ads"])

    def test_class_with_class_type(self):
        self.check_integration("test_class_with_class_type.h", [
            "test_namespace_with_class.ads",
            "test_class_in_namespace.ads",
            "test_class_with_class_type.ads"])
