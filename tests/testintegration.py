
import unittest
from capdpa import *

class Integration(unittest.TestCase):

    def compare(self, header, specs):
        result = []
        load = lambda spec: open("tests/data/" + spec, "r").read()
        cache = lambda res, spec: open("tests/cache/" + spec, "w").write(res)
        ada_spec = lambda ir: result.extend(ir.AdaSpecification()) if\
                type(ir.AdaSpecification()) == type([]) else\
                result.append(ir.AdaSpecification())
        check = lambda a, b: self.assertEqual(a, b, "Invalid entity: >>>\n" + a + "\n<<< expected: >>>\n" + b + "\n<<<")
#        print(CXX("tests/data/" + header).ToIR()[0].AdaSpecification())
        map(ada_spec, CXX("tests/data/" + header).ToIR())
        self.assertEqual(len(specs), len(result), "Expected {} compilation units, got {}\n====\n{}"
                .format(len(specs), len(result), result))
        map(cache, result, specs)
        map(check, result, map(load, specs))

    def test_empty_namespace(self):
        self.compare("test_empty_namespace.h", ["test_empty_namespace.ads"])

    def test_namespace_with_constants(self):
        self.compare(
                "test_namespace_with_constants.h",
                ["test_namespace_with_constants.ads"])

    def test_empty_class(self):
        self.compare(
                "test_empty_class.h",
                ["test_empty_class.ads"])

    def test_namespace_with_class(self):
        self.compare(
                "test_namespace_with_class.h",[
                    "test_namespace_with_class.ads",
                    "test_class_in_namespace.ads"])

    def test_namespace_with_enum(self):
        self.compare(
                "test_namespace_with_enum.h",
                ["test_namespace_with_enum.ads"])

    def test_class_with_constants(self):
        self.compare(
                "test_class_with_constants.h",
                ["test_class_with_constants.ads"])

    def test_class_with_members(self):
        self.compare(
                "test_class_with_members.h",
                ["test_class_with_members.ads"])

    def test_class_with_functions(self):
        self.compare(
                "test_class_with_functions.h",
                ["test_class_with_functions.ads"])

    def test_namespace_with_class_with_everything(self):
        self.compare("test_namespace_with_class_with_everything.h", [
            "test_namespace_with_class.ads",
            "test_namespace_with_class_with_everything.ads"])

    def test_class_with_class_type(self):
        self.compare("test_class_with_class_type.h", [
            "test_namespace_with_class.ads",
            "test_class_in_namespace.ads",
            "test_class_with_class_type.ads"])
