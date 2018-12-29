# -*- coding: utf-8 -*-

import unittest
from capdpa import *

class Mangling(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tests = CXX("tests/data/test_mangling.h").ToIR(project="Capdpa")

    def test_class_with_virtual(self):
        c = Class (name     = "With_Virtual",
                   children = [Function(name = "foo",
                                        parameters = None)])
        result = str(Namespace (name = "Capdpa", children = [c]).children[0].children[1].Mangle())
        self.assertTrue(result == "_ZN12With_Virtual3fooEv", "Invalid symbol: " + result)

    def test_class_with_functions_void (self):
        c = Class (name     = "With_functions",
                  children  = [Function(name = "public_function",
                                        parameters = [Variable (None, Type_Reference(name=Identifier(["Capdpa", "int"])))])])

        result = str(Namespace (name = "Capdpa", children = [c]).children[0].children[1].Mangle())
        self.assertTrue(result == "_ZN14With_functions15public_functionEi", "Invalid symbol: " + result)

    def test_class_with_functions_int (self):
        c = Class (name     = "With_functions",
                   children = [Function(name        = "named_param",
                                        parameters  = [Variable (Identifier(name=["Capdpa", "param"]), Type_Reference(name=Identifier(["Capdpa", "int"])))],
                                        return_type = Type_Reference(["int"]))])

        result = str(Namespace (name = "Capdpa", children = [c]).children[0].children[1].Mangle())
        self.assertTrue(result == "_ZN14With_functions11named_paramEi", "Invalid symbol: " + result)

    def test_class_with_functions_ctor (self):
        c = Class (name     = "With_functions",
                   children = [Constructor(parameters = None)])
        result = str(Namespace (name = "Capdpa", children = [c]).children[0].children[0].Mangle())
        self.assertTrue(result == "_ZN14With_functionsC1Ev", "Invalid symbol: " + result)

    def test_template_template_argument (self):
        symbol = str(self.tests["Cls", "bar"].Mangle())
        self.assertTrue (symbol == "_ZN3Cls3barE5TemplIciEc", "Invalid symbol: " + symbol)

    def test_template_no_template_argument (self):
        symbol = str(self.tests["Cls", "foo"].Mangle())
        self.assertTrue (symbol == "_ZN3Cls3fooEic", "Invalid symbol: " + symbol)

    def test_template_multiple_template_arguments (self):
        symbol = str(self.tests["Cls", "baz"].Mangle())
        self.assertTrue (symbol == "_ZN3Cls3bazE5TemplIciES0_IccE", "Invalid symbol: " + symbol)

    def EXCLUDE_test_template_4 (self):
        symbol = str(self.tests["Cls", "var"].Mangle())
        self.assertTrue (symbol == "_ZN3Cls3varE3VarIJEEc", "Invalid symbol: " + symbol)

    def test_compression_none (self):
        symbol = str(self.tests['Root2', 'Cls', 'no_compression'].Mangle())
        self.assertTrue (symbol == "_ZN5Root23Cls14no_compressionEii", "Invalid symbol: " + symbol)

    def test_compression1 (self):
        symbol = str(self.tests['Root2', 'Cls', 'compression1'].Mangle())
        self.assertTrue (symbol == "_ZN5Root23Cls12compression1EiNS_4DataE", "Invalid symbol: " + symbol)

    def test_compression2 (self):
        symbol = str(self.tests['Root2', 'Cls', 'compression2'].Mangle())
        self.assertTrue (symbol == "_ZN5Root23Cls12compression2ENS_4DataEiS1_", "Invalid symbol: " + symbol)

    def EXCLUDE_test_global_var (self):
        symbol = str(self.tests['global_var'].Mangle())
        self.assertTrue (symbol == "global_var", "Invalid symbol: " + symbol)

    def EXCLUDE_test_simple_var (self):
        symbol = str(self.tests['Root', 'simple_var'].Mangle())
        self.assertTrue (symbol == "_ZN4Root10simple_varE", "Invalid symbol: " + symbol)

    def EXCLUDE_test_global_fn(self):
        symbol = str(self.tests['global_fn'].Mangle())
        self.assertTrue (symbol == "global_fn", "Invalid symbol: " + symbol)

    def test_method_with_pointer(self):
        symbol = str(self.tests['Main', 'method_with_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main19method_with_pointerEPc", "Invalid symbol: " + symbol)

    def test_method_with_pointers(self):
        symbol = str(self.tests['Main', 'method_with_pointers'].Mangle())
        self.assertTrue (symbol == "_ZN4Main20method_with_pointersEPcPi", "Invalid symbol: " + symbol)

    def test_method_with_pointers_mixed(self):
        symbol = str(self.tests['Main', 'method_with_pointers_mixed'].Mangle())
        self.assertTrue (symbol == "_ZN4Main26method_with_pointers_mixedEPciPi", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return(self):
        symbol = str(self.tests['Main', 'method_with_pointer_return'].Mangle())
        self.assertTrue (symbol == "_ZN4Main26method_with_pointer_returnEv", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return_and_arg(self):
        symbol = str(self.tests['Main', 'method_with_pointer_return_and_arg'].Mangle())
        self.assertTrue (symbol == "_ZN4Main34method_with_pointer_return_and_argEPc", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return_and_args(self):
        symbol = str(self.tests['Main', 'method_with_pointer_return_and_args'].Mangle())
        self.assertTrue (symbol == "_ZN4Main35method_with_pointer_return_and_argsEPcPi", "Invalid symbol: " + symbol)

    def test_method_with_pointer_return_and_mixed(self):
        symbol = str(self.tests['Main', 'method_with_pointer_return_and_mixed'].Mangle())
        self.assertTrue (symbol == "_ZN4Main36method_with_pointer_return_and_mixedEPciPi", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer(self):
        symbol = str(self.tests['Main', 'method_with_class_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main25method_with_class_pointerEPN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointers(self):
        symbol = str(self.tests['Main', 'method_with_class_pointers'].Mangle())
        self.assertTrue (symbol == "_ZN4Main26method_with_class_pointersEPN4Root5Test1EPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointers_mixed(self):
        symbol = str(self.tests['Main', 'method_with_class_pointers_mixed'].Mangle())
        self.assertTrue (symbol == "_ZN4Main32method_with_class_pointers_mixedEPN4Root5Test1EiPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return(self):
        symbol = str(self.tests['Main', 'method_with_class_pointer_return'].Mangle())
        self.assertTrue (symbol == "_ZN4Main32method_with_class_pointer_returnEv", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return_and_arg(self):
        symbol = str(self.tests['Main', 'method_with_class_pointer_return_and_arg'].Mangle())
        self.assertTrue (symbol == "_ZN4Main40method_with_class_pointer_return_and_argEPN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return_and_args(self):
        symbol = str(self.tests['Main', 'method_with_class_pointer_return_and_args'].Mangle())
        self.assertTrue (symbol == "_ZN4Main41method_with_class_pointer_return_and_argsEPN4Root5Test1EPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_pointer_return_and_mixed(self):
        symbol = str(self.tests['Main', 'method_with_class_pointer_return_and_mixed'].Mangle())
        self.assertTrue (symbol == "_ZN4Main42method_with_class_pointer_return_and_mixedEPN4Root5Test1EiPNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference(self):
        symbol = str(self.tests['Main', 'method_with_class_reference'].Mangle())
        self.assertTrue (symbol == "_ZN4Main27method_with_class_referenceERN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_references(self):
        symbol = str(self.tests['Main', 'method_with_class_references'].Mangle())
        self.assertTrue (symbol == "_ZN4Main28method_with_class_referencesERN4Root5Test1ERNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_references_mixed(self):
        symbol = str(self.tests['Main', 'method_with_class_references_mixed'].Mangle())
        self.assertTrue (symbol == "_ZN4Main34method_with_class_references_mixedERN4Root5Test1EiRNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return(self):
        symbol = str(self.tests['Main', 'method_with_class_reference_return'].Mangle())
        self.assertTrue (symbol == "_ZN4Main34method_with_class_reference_returnEv", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return_and_arg(self):
        symbol = str(self.tests['Main', 'method_with_class_reference_return_and_arg'].Mangle())
        self.assertTrue (symbol == "_ZN4Main42method_with_class_reference_return_and_argERN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return_and_args(self):
        symbol = str(self.tests['Main', 'method_with_class_reference_return_and_args'].Mangle())
        self.assertTrue (symbol == "_ZN4Main43method_with_class_reference_return_and_argsERN4Root5Test1ERNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_class_reference_return_and_mixed(self):
        symbol = str(self.tests['Main', 'method_with_class_reference_return_and_mixed'].Mangle())
        self.assertTrue (symbol == "_ZN4Main44method_with_class_reference_return_and_mixedERN4Root5Test1EiRNS0_5Test2E", "Invalid symbol: " + symbol)

    def test_method_with_const_data_pointer(self):
        symbol = str(self.tests['Main', 'method_with_const_data_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main30method_with_const_data_pointerEPc", "Invalid symbol: " + symbol)

    def test_method_with_const_address_pointer(self):
        symbol = str(self.tests['Main', 'method_with_const_address_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main33method_with_const_address_pointerEPKc", "Invalid symbol: " + symbol)

    def test_method_with_const_data_const_address_pointer(self):
        symbol = str(self.tests['Main', 'method_with_const_data_const_address_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main44method_with_const_data_const_address_pointerEPKc", "Invalid symbol: " + symbol)

    def test_method_with_const_data_class_pointer(self):
        symbol = str(self.tests['Main', 'method_with_const_data_class_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main36method_with_const_data_class_pointerEPN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_const_address_class_pointer(self):
        symbol = str(self.tests['Main', 'method_with_const_address_class_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main39method_with_const_address_class_pointerEPKN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_const_data_const_address_class_pointer(self):
        symbol = str(self.tests['Main', 'method_with_const_data_const_address_class_pointer'].Mangle())
        self.assertTrue (symbol == "_ZN4Main50method_with_const_data_const_address_class_pointerEPKN4Root5Test1E", "Invalid symbol: " + symbol)

    def test_method_with_function_parameter(self):
        symbol = str(self.tests['Main', 'method_with_function_parameter'].Mangle())
        self.assertTrue (symbol == "_ZN4Main30method_with_function_parameterEPFPciE", "Invalid symbol: " + symbol)

    def test_method_with_function_parameters(self):
        symbol = str(self.tests['Main', 'method_with_function_parameters'].Mangle())
        self.assertTrue (symbol == "_ZN4Main31method_with_function_parametersEPFPciEPFicE", "Invalid symbol: " + symbol)

    def test_method_with_const_function_parameters(self):
        symbol = str(self.tests['Main', 'method_with_const_function_parameter'].Mangle())
        self.assertTrue (symbol == "_ZN4Main36method_with_const_function_parameterEPFPKciE", "Invalid symbol: " + symbol)

    def test_method_with_function_parameters_returning_value(self):
        symbol = str(self.tests['Main', 'method_with_function_parameter_returning_value'].Mangle())
        self.assertTrue (symbol == "_ZN4Main46method_with_function_parameter_returning_valueEPFlciE", "Invalid symbol: " + symbol)

    def test_method_with_parameterless_function_parameter(self):
        symbol = str(self.tests['Main', 'method_with_parameterless_function_parameter'].Mangle())
        self.assertTrue (symbol == "_ZN4Main44method_with_parameterless_function_parameterEPFmvE", "Invalid symbol: " + symbol)

    def test_method_with_function_reference(self):
        symbol = str(self.tests['Main', 'method_with_function_reference'].Mangle())
        self.assertTrue (symbol == "_ZN4Main30method_with_function_referenceERFPciE", "Invalid symbol: " + symbol)

    def test_method_complex(self):
        symbol = str(str(self.tests['Main', 'method_complex'].Mangle()))
        self.assertTrue (symbol == "_ZN4Main14method_complexEPFPvS0_EPFS0_PKvEPFS4_S0_E", "Invalid symbol: " + symbol)

    def test_method_with_function_paramters_substitution(self):
        symbol = str(self.tests['Main', 'method_with_function_paramters_substitution'].Mangle())
        self.assertTrue (symbol == "_ZN4Main43method_with_function_paramters_substitutionEPFPKvvEPFvS1_E", "Invalid symbol: " + symbol)

    def test_method_with_function_paramter_void_result(self):
        symbol = str(self.tests['Main', 'method_with_function_paramter_void_result'].Mangle())
        self.assertTrue (symbol == "_ZN4Main41method_with_function_paramter_void_resultEPFviE", "Invalid symbol: " + symbol)

    def test_method_with_function_paramter_const(self):
        symbol = str(self.tests['Main', 'method_with_function_paramter_const'].Mangle())
        self.assertTrue (symbol == "_ZN4Main35method_with_function_paramter_constEPFvPKvE", "Invalid symbol: " + symbol)

    def test_method_with_function_paramters_const_userdefined(self):
        symbol = str(self.tests['Main', 'method_with_function_paramters_const_userdefined'].Mangle())
        self.assertTrue (symbol == "_ZN4Main48method_with_function_paramters_const_userdefinedEPFvPKN4Root5Test1EPKNS0_5Test2ES3_E", "Invalid symbol: " + symbol)

    def test_method_with_function_paramters_const_ptr_subst(self):
        symbol = str(self.tests['Main', 'method_with_function_paramters_const_ptr_subst'].Mangle())
        self.assertTrue (symbol == "_ZN4Main46method_with_function_paramters_const_ptr_substEPFvPKN4Root5Test1ES3_PS1_E", "Invalid symbol: " + symbol)

    def test_method_with_function_paramters_const_ref_subst(self):
        symbol = str(self.tests['Main', 'method_with_function_paramters_const_ref_subst'].Mangle())
        self.assertTrue (symbol == "_ZN4Main46method_with_function_paramters_const_ref_substEPFvRKN4Root5Test2ES3_RS1_E", "Invalid symbol: " + symbol)

    def test_method_with_function_paramters_const_ref (self):
        symbol = str(self.tests['Main', 'method_with_function_paramters_const_ref'].Mangle())
        self.assertTrue (symbol == "_ZN4Main40method_with_function_paramters_const_refEPFvRKiE", "Invalid symbol: " + symbol)

    def test_method_with_function_paramters_const_ptr (self):
        symbol = str(self.tests['Main', 'method_with_function_paramters_const_ptr'].Mangle())
        self.assertTrue (symbol == "_ZN4Main40method_with_function_paramters_const_ptrEPFvPKiE", "Invalid symbol: " + symbol)

    # builtin tests

    def test_method_builtin_void (self):
        symbol = str(self.tests['Main', 'method_builtin_void'].Mangle())
        self.assertTrue (symbol == "_ZN4Main19method_builtin_voidEv", "Invalid symbol: " + symbol)

    def test_method_builtin_wchar_t (self):
        symbol = str(self.tests['Main', 'method_builtin_wchar_t'].Mangle())
        self.assertTrue (symbol == "_ZN4Main22method_builtin_wchar_tEw", "Invalid symbol: " + symbol)

    def test_method_builtin_bool (self):
        symbol = str(self.tests['Main', 'method_builtin_bool'].Mangle())
        self.assertTrue (symbol == "_ZN4Main19method_builtin_boolEb", "Invalid symbol: " + symbol)

    def test_method_builtin_char (self):
        symbol = str(self.tests['Main', 'method_builtin_char'].Mangle())
        self.assertTrue (symbol == "_ZN4Main19method_builtin_charEc", "Invalid symbol: " + symbol)

    def test_method_builtin_signed_char (self):
        symbol = str(self.tests['Main', 'method_builtin_signed_char'].Mangle())
        self.assertTrue (symbol == "_ZN4Main26method_builtin_signed_charEa", "Invalid symbol: " + symbol)

    def test_method_builtin_unsigned_char (self):
        symbol = str(self.tests['Main', 'method_builtin_unsigned_char'].Mangle())
        self.assertTrue (symbol == "_ZN4Main28method_builtin_unsigned_charEh", "Invalid symbol: " + symbol)

    def test_method_builtin_short (self):
        symbol = str(self.tests['Main', 'method_builtin_short'].Mangle())
        self.assertTrue (symbol == "_ZN4Main20method_builtin_shortEs", "Invalid symbol: " + symbol)

    def test_method_builtin_unsigned_short (self):
        symbol = str(self.tests['Main', 'method_builtin_unsigned_short'].Mangle())
        self.assertTrue (symbol == "_ZN4Main29method_builtin_unsigned_shortEt", "Invalid symbol: " + symbol)

    def test_method_builtin_int (self):
        symbol = str(self.tests['Main', 'method_builtin_int'].Mangle())
        self.assertTrue (symbol == "_ZN4Main18method_builtin_intEi", "Invalid symbol: " + symbol)

    def test_method_builtin_unsigned_int (self):
        symbol = str(self.tests['Main', 'method_builtin_unsigned_int'].Mangle())
        self.assertTrue (symbol == "_ZN4Main27method_builtin_unsigned_intEj", "Invalid symbol: " + symbol)

    def test_method_builtin_long (self):
        symbol = str(self.tests['Main', 'method_builtin_long'].Mangle())
        self.assertTrue (symbol == "_ZN4Main19method_builtin_longEl", "Invalid symbol: " + symbol)

    def test_method_builtin_unsigned_long (self):
        symbol = str(self.tests['Main', 'method_builtin_unsigned_long'].Mangle())
        self.assertTrue (symbol == "_ZN4Main28method_builtin_unsigned_longEm", "Invalid symbol: " + symbol)

    def test_method_builtin_long_long (self):
        symbol = str(self.tests['Main', 'method_builtin_long_long'].Mangle())
        self.assertTrue (symbol == "_ZN4Main24method_builtin_long_longEx", "Invalid symbol: " + symbol)

    def test_method_builtin_unsigned_long_long (self):
        symbol = str(self.tests['Main', 'method_builtin_unsigned_long_long'].Mangle())
        self.assertTrue (symbol == "_ZN4Main33method_builtin_unsigned_long_longEy", "Invalid symbol: " + symbol)

    def test_method_builtin___int128 (self):
        symbol = str(self.tests['Main', 'method_builtin___int128'].Mangle())
        self.assertTrue (symbol == "_ZN4Main23method_builtin___int128En", "Invalid symbol: " + symbol)

    def test_method_builtin_unsigned__int128 (self):
        symbol = str(self.tests['Main', 'method_builtin_unsigned__int128'].Mangle())
        self.assertTrue (symbol == "_ZN4Main31method_builtin_unsigned__int128Eo", "Invalid symbol: " + symbol)

    def test_method_builtin_float (self):
        symbol = str(self.tests['Main', 'method_builtin_float'].Mangle())
        self.assertTrue (symbol == "_ZN4Main20method_builtin_floatEf", "Invalid symbol: " + symbol)

    def test_method_builtin_double (self):
        symbol = str(self.tests['Main', 'method_builtin_double'].Mangle())
        self.assertTrue (symbol == "_ZN4Main21method_builtin_doubleEd", "Invalid symbol: " + symbol)

    def test_method_builtin_long_double (self):
        symbol = str(self.tests['Main', 'method_builtin_long_double'].Mangle())
        self.assertTrue (symbol == "_ZN4Main26method_builtin_long_doubleEe", "Invalid symbol: " + symbol)

    # FIXME: __float128 is not supported in the Clang version we are using (returns INT)
    def EXCLUDE_test_method_builtin___float128 (self):
        symbol = str(self.tests['Main', 'method_builtin___float128'].Mangle())
        self.assertTrue (symbol == "_ZN4Main25method_builtin___float128Eg", "Invalid symbol: " + symbol)

    def test_multiple_constructors (self):
        symbol = str(self.tests['Bar', 'Foo'].children[0].Mangle())
        self.assertTrue (symbol == "_ZN3Bar3FooC1Ei", "Invalid symbol: " + symbol)
        symbol = str(self.tests['Bar', 'Foo'].children[1].Mangle())
        self.assertTrue (symbol == "_ZN3Bar3FooC1Ec", "Invalid symbol: " + symbol)

    # Template instances
    def test_template_instance (self):
        symbol = str(self.tests['Templ1', 'Blubber_T_int', 'foo'].Mangle())
        self.assertTrue (symbol == "_ZN6Templ17BlubberIiE3fooES1_", "Invalid symbol: " + symbol)

    def test_template_instance_multi (self):
        symbol = str(self.tests['Templ1', 'B_T_char_int', 'foo'].Mangle())
        self.assertTrue (symbol == "_ZN6Templ11BIciE3fooEcS1_i", "Invalid symbol: " + symbol)

    def EXCLUDE_test_template_instance_complex (self):
        symbol = str(self.tests['Templ2', ['Cde_T_char_int', 'foo']].Mangle())
        self.assertTrue (symbol == "_ZN6Templ23CdeIcN3Bar3FooEE3fooEcS3_i", "Invalid symbol: " + symbol)

    # ::std namespace tests -- NOT IMPLEMENTED
    def EXCLUDE_test_std_namespace(self):
        symbol = self.tests['std', 'Foo', 'std_namespace'].Mangle()
        self.assertTrue (symbol == "_ZNSt3Foo13std_namespaceEc", "Invalid symbol: " + symbol)

    # Missing:
    #   * Template parameters (T_, T0_, ...)
    #   * Encoding for standard namespaces

if __name__ == '__main__':
    unittest.main()
