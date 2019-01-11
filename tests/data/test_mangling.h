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
      char *method_with_pointer_return () { return (char *)0; };
      char *method_with_pointer_return_and_arg (char *ptr) { return (char *)0; };
      char *method_with_pointer_return_and_args (char *ptr1, int *ptr2) { return (char *)0; };
      char *method_with_pointer_return_and_mixed (char *ptr1, int value, int *ptr2) { return (char *)0; };

      void method_with_class_pointer (Root::Test1 *ptr) { };
      void method_with_class_pointers (Root::Test1 *ptr1, Root::Test2 *ptr2) { };
      void method_with_class_pointers_mixed (Root::Test1 *ptr1, int value, Root::Test2 *ptr2) { };
      Root::Test1 *method_with_class_pointer_return () { return (Root::Test1 *)0; };
      Root::Test1 *method_with_class_pointer_return_and_arg (Root::Test1 *ptr) { return (Root::Test1 *)0;};
      Root::Test1 *method_with_class_pointer_return_and_args (Root::Test1 *ptr1, Root::Test2 *ptr2) { return (Root::Test1 *)0;};
      Root::Test1 *method_with_class_pointer_return_and_mixed (Root::Test1 *ptr1, int value, Root::Test2 *ptr2) { return (Root::Test1 *)0;};

      void method_with_class_reference (Root::Test1& ref) { };
      void method_with_class_references (Root::Test1& ref1, Root::Test2& ref2) { };
      void method_with_class_references_mixed (Root::Test1& ref1, int value, Root::Test2& ref2) { };
      Root::Test1& method_with_class_reference_return () { return *(new Root::Test1); };
      Root::Test1& method_with_class_reference_return_and_arg (Root::Test1& ref) { return *(new Root::Test1); };
      Root::Test1& method_with_class_reference_return_and_args (Root::Test1& ref1, Root::Test2& ref2) { return *(new Root::Test1); };
      Root::Test1& method_with_class_reference_return_and_mixed (Root::Test1& ref1, int value, Root::Test2& ref2) { return *(new Root::Test1); };

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
      void method_with_function_paramters_const_ref(void (*)(const int&)) { };
      void method_with_function_paramters_const_ptr(void (*)(const int *)) { };

      void method_builtin_void (void) { };
      void method_builtin_wchar_t (wchar_t) { };
      void method_builtin_bool (bool) { };
      void method_builtin_char (char) { };
      void method_builtin_signed_char (signed char) { };
      void method_builtin_unsigned_char (unsigned char) { };
      void method_builtin_short (short) { };
      void method_builtin_unsigned_short (unsigned short) { };
      void method_builtin_int (int) { };
      void method_builtin_unsigned_int (unsigned int) { };
      void method_builtin_long (long) { };
      void method_builtin_unsigned_long (unsigned long) { };
      void method_builtin_long_long (long long) { };
      void method_builtin_unsigned_long_long (unsigned long long) { };
      void method_builtin___int128 (__int128) { };
      void method_builtin_unsigned__int128 (unsigned __int128) { };
      void method_builtin_float (float) { };
      void method_builtin_double (double) { };
      void method_builtin_long_double (long double) { };
};

namespace std {
   class Foo
   {
      public:
         void std_namespace (char foo) { };
   };
}

namespace Bar {
   class Foo
   {
      public:
         Foo (int arg) { };
         Foo (char arg) { };
   };
}

namespace Templ1 {

   template<typename T>
   struct Blubber {
      void foo(Blubber);
      Blubber() { };
   };

   template<typename T, typename J>
   struct B {
      void foo(char, B, int);
   };

   template<> void Blubber<int>::foo(Blubber<int>) {};
   template<> void B<char, int>::foo(char, B<char, int>, int) {};
}

namespace Templ2 {

   template<typename T, typename J>
   struct Cde {
      void foo(char, Cde, int);
   };


   // template<> void Cde<char, Bar::Foo>::foo(char, Cde<char, Bar::Foo>, int) {};
}

template <typename A, typename B>
class Templ
{
   public:
      Templ() { };
      A element1;
      B element2;
};

template <typename ...Ts>
class Var
{
   public:
      Var() { };
      int element1;
};

class Cls
{
   public:
      Cls() { };
      int bar (Templ<char, int> p1, char p2) { return 0; };
      int foo (int p1, char p2) { return 0; };
      int baz (Templ<char, int> p1, Templ<char,char> p2) { return 0; };
      // int var (Var<> p1, char p2) { };
};

namespace Root2
{
   class Data {
      public:
         int elem;
   };

   class Cls {
      public:
         int no_compression (int p1, int p2) { return 0; };
         Data compression1 (int p1, Data p2) { return *(new Data); };
         int compression2 (Data p1, int p2, Data p3) { return 0; };
   };
}
