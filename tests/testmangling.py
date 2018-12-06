# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class Mangling(unittest.TestCase):

    def setUp(self):
        self.mangling    = CXX("tests/data/test_mangling.h").ToIR(project="Capdpa").children
        self.templates   = CXX("tests/data/test_template_mangling.h").ToIR(project="Capdpa").children
        self.compression = CXX("tests/data/mangling_compression.h").ToIR(project="Capdpa").children

    def test_class_with_virtual(self):
        c = Class (name     = "With_Virtual",
                   children = [Function(name = "foo",
                                        symbol     = "",
                                        parameters = None)])
        result = Namespace (name = "Capdpa", children = [c]).children[0].children[1].Mangle("Capdpa")
        self.assertTrue(result == "_ZN12With_Virtual3fooEv", "Invalid symbol: " + result)

    def test_class_with_functions_void (self):
        c = Class (name     = "With_functions",
                  children  = [Function(name = "public_function",
                                        symbol     = "",
                                        parameters = [Variable (None, Type_Reference(name=Identifier(["Capdpa", "int"])))])])

        result = Namespace (name = "Capdpa", children = [c]).children[0].children[1].Mangle("Capdpa")
        self.assertTrue(result == "_ZN14With_functions15public_functionEi", "Invalid symbol: " + result)

    def test_class_with_functions_int (self):
        c = Class (name     = "With_functions",
                   children = [Function(name        = "named_param",
                                        symbol      = "",
                                        parameters  = [Variable (Identifier(name=["Capdpa", "param"]), Type_Reference(name=Identifier(["Capdpa", "int"])))],
                                        return_type = Type_Reference(["int"]))])

        result = Namespace (name = "Capdpa", children = [c]).children[0].children[1].Mangle("Capdpa")
        self.assertTrue(result == "_ZN14With_functions11named_paramEi", "Invalid symbol: " + result)

    def test_class_with_functions_ctor (self):
        c = Class (name     = "With_functions",
                   children = [Constructor(symbol     = "",
                                           parameters = None)])
        result = Namespace (name = "Capdpa", children = [c]).children[0].children[0].Mangle("Capdpa")
        self.assertTrue(result == "_ZN14With_functionsC1Ev", "Invalid symbol: " + result)

    def test_template_template_argument (self):
        symbol = self.templates[2].children[1].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN3Cls3barE5TemplIciEc", "Invalid symbol: " + symbol)

    def test_template_no_template_argument (self):
        symbol = self.templates[2].children[2].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN3Cls3fooEic", "Invalid symbol: " + symbol)

    def test_template_multiple_template_arguments (self):
        symbol = self.templates[2].children[3].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN3Cls3bazE5TemplIciES0_IccE", "Invalid symbol: " + symbol)

    def EXCLUDE_test_template_4 (self):
        symbol = self.templates[0].children[1].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN3Cls3varE3VarIJEEc", "Invalid symbol: " + symbol)

    def test_compression_none (self):
        symbol = self.compression[0].children[1].children[1].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Root3Cls14no_compressionEii", "Invalid symbol: " + symbol)

    def test_compression1 (self):
        symbol = self.compression[0].children[1].children[2].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Root3Cls12compression1EiNS_4DataE", "Invalid symbol: " + symbol)

    def test_compression2 (self):
        symbol = self.compression[0].children[1].children[3].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Root3Cls12compression2ENS_4DataEiS1_", "Invalid symbol: " + symbol)

    def EXCLUDE_test_global_var (self):
        symbol = self.mangling[0].children[0].Mangle("Capdpa")
        self.assertTrue (symbol == "global_var", "Invalid symbol: " + symbol)

    def EXCLUDE_test_simple_var (self):
        symbol = self.mangling[0].children[0].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Root10simple_varE", "Invalid symbol: " + symbol)

    def EXCLUDE_test_global_fn(self):
        symbol = self.mangling[0].children[0].Mangle("Capdpa")
        self.assertTrue (symbol == "global_fn", "Invalid symbol: " + symbol)

    def test_method_with_pointer(self):
        symbol = self.mangling[1].children[1].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main19method_with_pointerEPc", "Invalid symbol: " + symbol)

    def test_method_with_pointers(self):
        symbol = self.mangling[1].children[2].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main20method_with_pointersEPcPi", "Invalid symbol: " + symbol)

    def test_method_with_pointers_mixed(self):
        symbol = self.mangling[1].children[3].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main26method_with_pointers_mixedEPciPi", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return(self):
        symbol = self.mangling[1].children[4].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main26method_with_pointer_returnEv", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return_and_arg(self):
        symbol = self.mangling[1].children[5].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main34method_with_pointer_return_and_argEPc", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return_and_args(self):
        symbol = self.mangling[1].children[6].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main35method_with_pointer_return_and_argsEPcPi", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return_and_mixed(self):
        symbol = self.mangling[1].children[7].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main36method_with_pointer_return_and_mixedEPciPi", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer(self):
        symbol = self.mangling[1].children[8].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main25method_with_class_pointerEPN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointers(self):
        symbol = self.mangling[1].children[9].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main26method_with_class_pointersEPN4Root5Test1EPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointers_mixed(self):
        symbol = self.mangling[1].children[10].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main32method_with_class_pointers_mixedEPN4Root5Test1EiPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return(self):
        symbol = self.mangling[1].children[11].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main32method_with_class_pointer_returnEv", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return_and_arg(self):
        symbol = self.mangling[1].children[12].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main40method_with_class_pointer_return_and_argEPN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return_and_args(self):
        symbol = self.mangling[1].children[13].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main41method_with_class_pointer_return_and_argsEPN4Root5Test1EPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return_and_mixed(self):
        symbol = self.mangling[1].children[14].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main42method_with_class_pointer_return_and_mixedEPN4Root5Test1EiPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference(self):
        symbol = self.mangling[1].children[15].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main27method_with_class_referenceERN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_references(self):
        symbol = self.mangling[1].children[16].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main28method_with_class_referencesERN4Root5Test1ERNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_references_mixed(self):
        symbol = self.mangling[1].children[17].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main34method_with_class_references_mixedERN4Root5Test1EiRNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return(self):
        symbol = self.mangling[1].children[18].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main34method_with_class_reference_returnEv", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return_and_arg(self):
        symbol = self.mangling[1].children[19].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main42method_with_class_reference_return_and_argERN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return_and_args(self):
        symbol = self.mangling[1].children[20].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main43method_with_class_reference_return_and_argsERN4Root5Test1ERNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return_and_mixed(self):
        symbol = self.mangling[1].children[21].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main44method_with_class_reference_return_and_mixedERN4Root5Test1EiRNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_const_data_pointer(self):
        symbol = self.mangling[1].children[22].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main30method_with_const_data_pointerEPc", "Invalid symbol: " + symbol)

    def test_method_with_const_address_pointer(self):
        symbol = self.mangling[1].children[23].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main33method_with_const_address_pointerEPKc", "Invalid symbol: " + symbol)

    def test_method_with_const_data_const_address_pointer(self):
        symbol = self.mangling[1].children[24].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main44method_with_const_data_const_address_pointerEPKc", "Invalid symbol: " + symbol)

    def test_method_with_const_data_class_pointer(self):
        symbol = self.mangling[1].children[25].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main36method_with_const_data_class_pointerEPN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_const_address_class_pointer(self):
        symbol = self.mangling[1].children[26].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main39method_with_const_address_class_pointerEPKN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_const_data_const_address_class_pointer(self):
        symbol = self.mangling[1].children[27].Mangle("Capdpa")
        self.assertTrue (symbol == "_ZN4Main50method_with_const_data_const_address_class_pointerEPKN4Root5Test1E", "Invalid symbol: " + symbol)
