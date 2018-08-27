
import unittest
from capdpa import *

class Parser(unittest.TestCase):

    def test_empty_namespace(self):
        expected = Namespace(name = Identifier(["Empty"]))
        result = CXX("tests/data/test_empty_namespace.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_namespace_with_constants(self):
        expected = Namespace(name = Identifier(["With_constants"]),
                constants = [Constant(name = Identifier(["X"]), value = 1),
                    Constant(name = Identifier(["Y"]), value = 2),
                    Constant(name = Identifier(["Z"]), value = 3)])
        result = CXX("tests/data/test_namespace_with_constants.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_empty_class(self):
        expected = Class(name = Identifier(["Empty"]))
        result = CXX("tests/data/test_empty_class.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_namespace_with_class(self):
        expected = Namespace (name = Identifier(["With_class"]),
                classes = [Class(name = Identifier(["In_namespace"]))])
        result = CXX("tests/data/test_empty_class.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_namespace_with_enum(self):
        expected = Namespace (name = Identifier(["With_enum"]),
                enums = [Enum(name = Identifier(["Constants"]),
                    constants = [
                        Constant(name = Identifier(["ONE"]), value = 1),
                        Constant(name = Identifier(["TWO"]), value = 2),
                        Constant(name = Identifier(["THREE"]), value = 3)])])
        result = CXX("tests/data/test_namespace_with_enum.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_class_with_constants(self):
        expected = Class (name = Identifier(["With_constants"]),
                constants = [Constant(name = Identifier(["ONE"]), value = 1),
                    Constant(name = Identifier(["TWO"]), value = 2),
                    Constant(name = Identifier(["THREE"]), value = 3)],
                enums = [Enum(name = Identifier(["NEGATIVE"]), constants = [
                    Constant(name = Identifier(["ONE"]), value = -1),
                    Constant(name = Identifier(["TWO"]), value = -2),
                    Constant(name = Identifier(["THREE"]), value = -3)])])
        result = CXX("tests/data/test_class_with_constants.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_class_with_members(self):
        expected = Class(name = Identifier(["With_members"]),
                members = [
                    Variable (name = Identifier(["public_int"]), ctype = Type(name = Identifier(["int"]), size = 4)),
                    Variable (name = Identifier(["public_pointer"]), ctype = Type(name = Identifier(["void *"]), size = 8)),
                    Variable (name = Identifier(["public_float"]), ctype = Type(name = Identifier(["float"]), size = 4))])
        result = CXX("tests/data/test_class_with_members.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_class_with_functions(self):
        expected = Class(name = Identifier(["With_functions"]),
                functions = [
                    Function(name = Identifier(["public_function"]), symbol = "", parameters = [
                        Variable (name = Identifier(["arg1"]), ctype = Type(name = Identifier(["int"]), size = 4))]),
                    Function(name = Identifier(["named_param"]), symbol = "", parameters = [
                        Variable (name = Identifier(["param"]), ctype = Type(name = Identifier(["int"]), size = 4))],
                        )],
                constructors = [Function(name = Identifier(["With_functions"]), symbol = "")])
        result = CXX("tests/data/test_class_with_functions.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

    def test_namespace_with_class_with_everything(self):
        expected = Namespace(name = Identifier(["With_class"]), classes = [
            Class(name = Identifier(["With_everything"]),
                constants = [
                    Constant(name = Identifier(["ONE"]), value = 1),
                    Constant(name = Identifier(["TWO"]), value = 2)],
                enums = [
                    Enum(name = Identifier(["NEGATIVE"]), constants = [
                        Constant(name = Identifier(["ONE"]), value = -1),
                        Constant(name = Identifier(["TWO"]), value = -2)])],
                functions = [
                    Function(name = Identifier(["public_function"]), symbol = "")],
                members = [
                    Variable(name = Identifier(["public_int"]), ctype = Type(name = Identifier(["int"]), size = 4))],
                constructors = [Function(name = Identifier(["With_everything"]), symbol = "")])])
        result = CXX("tests/data/test_namespace_with_class_with_everything.h").ToIR()
        self.assertEqual(result, expected, "Expected " + str(expected.__dict__) + " got " + str(result.__dict__))

