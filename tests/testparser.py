
import unittest
from capdpa import *

class Parser(unittest.TestCase):

    def xtest_empty_namespace(self):
        expected = Namespace(name = "Empty")
        result = CXX("tests/data/test_empty_namespace.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_namespace_with_constants(self):
        expected = Namespace(name = "With_constants",
                constants = [Constant(name = "X", value = 1),
                    Constant(name = "Y", value = 2),
                    Constant(name = "Z", value = 3)])
        result = CXX("tests/data/test_namespace_with_constants.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_empty_class(self):
        expected = Class(name = "Empty")
        result = CXX("tests/data/test_empty_class.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_namespace_with_class(self):
        expected = Namespace (name = "With_class",
                classes = [Class(name = "In_namespace")])
        result = CXX("tests/data/test_namespace_with_class.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_namespace_with_enum(self):
        expected = Namespace (name = "With_enum",
                enums = [Enum(name = "Constants",
                    constants = [
                        Constant(name = "ONE", value = 1),
                        Constant(name = "TWO", value = 2),
                        Constant(name = "THREE", value = 3)])])
        result = CXX("tests/data/test_namespace_with_enum.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_class_with_constants(self):
        expected = Class (name = "With_constants",
                constants = [Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Constant(name = "THREE", value = 3)],
                enums = [Enum(name = "NEGATIVE", constants = [
                    Constant(name = "MINUS_ONE", value = -1),
                    Constant(name = "MINUS_TWO", value = -2),
                    Constant(name = "MINUS_THREE", value = -3)])])
        result = CXX("tests/data/test_class_with_constants.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_class_with_members(self):
        expected = Class(name = "With_members",
                members = [
                    Variable (name = "public_int", ctype = Type_Reference(name = Identifier(["int"]))),
                    Variable (name = "public_pointer", ctype = Type_Reference(name = Identifier(["void *"]))),
                    Variable (name = "public_float", ctype = Type_Reference(name = Identifier(["float"])))])
        result = CXX("tests/data/test_class_with_members.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_class_with_functions(self):
        expected = Class(name = "With_functions",
                functions = [
                    Function(name = "public_function", symbol = "", parameters = [
                        Variable (name = "arg1", ctype = Type_Reference(name = Identifier(["int"])))]),
                    Function(name = "named_param", symbol = "", parameters = [
                        Variable (name = "param", ctype = Type_Reference(name = Identifier(["int"])))],
                        return_type = Type_Reference(name = Identifier(["int"]))
                        )],
                constructors = [Function(name = "With_functions", symbol = "")])
        result = CXX("tests/data/test_class_with_functions.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def xtest_namespace_with_class_with_everything(self):
        expected = Namespace(name = "With_class", classes = [
            Class(name = "With_everything",
                constants = [
                    Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2)],
                enums = [
                    Enum(name = "NEGATIVE", constants = [
                        Constant(name = "MINUS_ONE", value = -1),
                        Constant(name = "MINUS_TWO", value = -2)])],
                functions = [
                    Function(name = "public_function", symbol = "")],
                members = [
                    Variable(name = "public_int", ctype = Type_Reference(name = Identifier(["int"])))],
                constructors = [Function(name = "With_everything", symbol = "")])])
        result = CXX("tests/data/test_namespace_with_class_with_everything.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_class_with_class_type(self):
        expected = Class(name = "Full",
                members = [
                        Variable(name = "value", ctype = Type_Reference(name = Identifier(["With_class", "In_namespace"])))
                    ])
        result = CXX("tests/data/test_class_with_class_type.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))
