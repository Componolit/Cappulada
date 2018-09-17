
import unittest
from capdpa import *

class Parser(unittest.TestCase):

    def test_empty_namespace(self):
        expected = [Namespace(name = "Empty")]
        result = CXX("tests/data/test_empty_namespace.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_namespace_with_constants(self):
        expected = [Namespace(name = "With_constants",
            children = [
                Constant(name = "X", value = 1),
                Constant(name = "Y", value = 2),
                Constant(name = "Z", value = 3)])]
        result = CXX("tests/data/test_namespace_with_constants.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_empty_class(self):
        expected = [Class(name = "Empty")]
        result = CXX("tests/data/test_empty_class.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_namespace_with_class(self):
        expected = [Namespace (name = "With_class",
                children = [Class(name = "In_namespace")])]
        result = CXX("tests/data/test_namespace_with_class.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_namespace_with_enum(self):
        expected = [Namespace (name = "With_enum",
                children = [Enum(name = "Constants",
                    children = [
                        Constant(name = "ONE", value = 1),
                        Constant(name = "TWO", value = 2),
                        Constant(name = "THREE", value = 3)])])]
        result = CXX("tests/data/test_namespace_with_enum.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_class_with_constants(self):
        expected = [Class (name = "With_constants",
                children = [Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Constant(name = "THREE", value = 3),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_ONE", value = -1),
                        Constant(name = "MINUS_TWO", value = -2),
                        Constant(name = "MINUS_THREE", value = -3)])])]
        result = CXX("tests/data/test_class_with_constants.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_class_with_members(self):
        expected = [Class(name = "With_members",
                children = [
                    Variable (name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "Types", "int"]))),
                    Variable (name = "public_pointer", ctype = Type_Reference(name = Identifier(["void"]), pointer = 1)),
                    Variable (name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "Types", "C_float"])))])]
        result = CXX("tests/data/test_class_with_members.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_class_with_functions(self):
        expected = [Class(name = "With_functions",
                children = [
                    Function(name = "public_function", symbol = "", parameters = [
                        Variable (name = "arg1", ctype = Type_Reference(name = Identifier(["Capdpa", "Types", "int"])))]),
                    Function(name = "named_param", symbol = "", parameters = [
                        Variable (name = "param", ctype = Type_Reference(name = Identifier(["Capdpa", "Types", "int"])))],
                        return_type = Type_Reference(name = Identifier(["Capdpa", "Types", "int"]))
                        ),
                    Constructor(name = "With_functions", symbol = "")])]
        result = CXX("tests/data/test_class_with_functions.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_namespace_with_class_with_everything(self):
        expected = [Namespace(name = "With_class", children = [
            Class(name = "With_everything",
                children = [
                    Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_ONE", value = -1),
                        Constant(name = "MINUS_TWO", value = -2)]),
                    Function(name = "public_function", symbol = ""),
                    Variable(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "Types", "int"]))),
                    Constructor(name = "With_everything", symbol = "")])])]
        result = CXX("tests/data/test_namespace_with_class_with_everything.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_class_with_class_type(self):
        expected = [
                Namespace (name = "With_class",
                    children = [Class(name = "In_namespace")]),
                Class(name = "Full",
                    children = [
                        Variable(name = "value", ctype = Type_Reference(name = Identifier(["With_class", "In_namespace"]), builtin = False)),
                        Variable(name = "value_ptr", ctype = Type_Reference(name = Identifier(["With_class", "In_namespace"]), pointer = 1, builtin = False))
                    ])]
        result = CXX("tests/data/test_class_with_class_type.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))

    def test_types(self):
        expected = [
                Type_Definition(
                    name="uint8_t",
                    reference=Type_Reference(name=Identifier(name=["Capdpa", "Types", "unsigned_char"]), pointer=0, builtin=True)),
                Type_Definition(
                    name="int32_t",
                    reference=Type_Reference(name=Identifier(name=["Capdpa", "Types", "int"]), pointer=0, builtin=True)),
                Type_Definition(name="u8", reference=Type_Reference(name=Identifier(name=["uint8_t"]), pointer=0, builtin=False))]
        result = CXX("tests/data/test_types.h").ToIR()
        self.assertEqual(result, expected, "Expected \n" + str(expected) + "\n got \n" + str(result))
