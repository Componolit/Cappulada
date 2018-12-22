namespace Foo {

   class Bar { };

   template<typename T>
   struct Baz {
      void fun(Baz);
   };

   template<> void Baz<Bar>::fun(Baz<Bar>) {};
}
