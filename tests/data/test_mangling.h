int global_var;
void(*global_fn)(int);

namespace Root
{
   int simple_var;

   class Test1 { };
   class Test2 { };
}

class Main
{
   public:
      void method_with_pointer (char *ptr) { };
      void method_with_pointers (char *ptr1, int *ptr2) { };
      void method_with_pointers_mixed (char *ptr1, int value, int *ptr2) { };
      char *method_with_pointer_return () { };
      char *method_with_pointer_return_and_arg (char *ptr) { };
      char *method_with_pointer_return_and_args (char *ptr1, int *ptr2) { };
      char *method_with_pointer_return_and_mixed (char *ptr1, int value, int *ptr2) { };

      void method_with_class_pointer (Root::Test1 *ptr) { };
      void method_with_class_pointers (Root::Test1 *ptr1, Root::Test2 *ptr2) { };
      void method_with_class_pointers_mixed (Root::Test1 *ptr1, int value, Root::Test2 *ptr2) { };
      Root::Test1 *method_with_class_pointer_return () { };
      Root::Test1 *method_with_class_pointer_return_and_arg (Root::Test1 *ptr) { };
      Root::Test1 *method_with_class_pointer_return_and_args (Root::Test1 *ptr1, Root::Test2 *ptr2) { };
      Root::Test1 *method_with_class_pointer_return_and_mixed (Root::Test1 *ptr1, int value, Root::Test2 *ptr2) { };

      void method_with_class_reference (Root::Test1& ref) { };
      void method_with_class_references (Root::Test1& ref1, Root::Test2& ref2) { };
      void method_with_class_references_mixed (Root::Test1& ref1, int value, Root::Test2& ref2) { };
      Root::Test1& method_with_class_reference_return () { };
      Root::Test1& method_with_class_reference_return_and_arg (Root::Test1& ref) { };
      Root::Test1& method_with_class_reference_return_and_args (Root::Test1& ref1, Root::Test2& ref2) { };
      Root::Test1& method_with_class_reference_return_and_mixed (Root::Test1& ref1, int value, Root::Test2& ref2) { };

      void method_with_const_data_pointer (char * const ptr) { };
      void method_with_const_address_pointer (const char * ptr) { };
      void method_with_const_data_const_address_pointer (const char * const ptr) { };
      void method_with_const_data_class_pointer (Root::Test1 * const ptr) { };
      void method_with_const_address_class_pointer (const Root::Test1 * ptr) { };
      void method_with_const_data_const_address_class_pointer (const Root::Test1 * const ptr) { };

      void method_with_function_parameter (char *(*fn)(int)) { };
      void method_with_function_parameters (char *(*fn1)(int), int (*fn2)(char)) { };
      void method_with_const_function_parameter (const char *(*fn)(int)) { };
      void method_with_function_parameter_returning_value (long (*fn)(char, int)) { };
      void method_with_parameterless_function_parameter (unsigned long (*fn)()) { };

      void method_with_function_reference (char *(&fn)(int)) { };

      void method_complex(void* (*)(void*), void* (*)(const void*), const void* (*)(void*)) { };
      void method_with_function_paramters_substitution(const void* (*)(void), void (*)(const void *)) { };
      void method_with_function_paramter_void_result(void (*)(int)) { };
      void method_with_function_paramter_const(void (*)(const void *)) { };
      void method_with_function_paramters_const_userdefined(void (*)(const Root::Test1 *, const Root::Test2 *, const Root::Test1 *)) { };

      void method_with_function_paramters_const_ptr_subst(void (*)(const Root::Test1 *, const Root::Test1 *, Root::Test1 *)) { };
      void method_with_function_paramters_const_ref_subst(void (*)(const Root::Test2&, const Root::Test2&, Root::Test2&)) { };
};

namespace std {
   class Foo
   {
      public:
         void std_namespace (char foo) { };
   };
}
