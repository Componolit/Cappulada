
import unittest
from cxx_types import number

class TypeTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def print_namespace(self, indentation, namespace):
        print(" " * indentation + namespace.name)
        for n in namespace.namespaces:
            self.print_namespace(indentation + 2, n)
        for c in namespace.classes:
            self.print_class(indentation + 2, c)
        for c in namespace.constants:
            self.print_constant(indentation + 2, c)
        for e in namespace.enums:
            print(" " * (indentation + 2) + e.name)
            for c in e.constants:
                self.print_constant(indentation + 4, c)

    def print_class(self, indentation, cl):
        print(" " * indentation + cl.name)
        self.print_function(indentation + 2, cl.constructor)
        for m in cl.members:
            self.print_variable(indentation + 2, m)
        for f in cl.functions:
            self.print_function(indentation + 2, f)

    def print_constant(self, indentation, c):
        print(" " * indentation + c.name + ": " + str(c.value))

    def print_variable(self, indentation, v):
        print(" " * indentation + v.name + " : " + v.ctype.name)

    def print_function(self, indentation, f):
        print(" " * indentation + f.name + " -> " + f.return_type.name)
        for a in f.parameters:
            self.print_variable(indentation + 2, a)


    def xtest_number(self):
        self.print_namespace(0, number)
