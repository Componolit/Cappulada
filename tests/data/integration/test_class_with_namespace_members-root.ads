with Test_Class_With_Namespace_Members.Foo;

package Test_Class_With_Namespace_Members.Root
   with SPARK_Mode => On
is
   package Baz
      with SPARK_Mode => On
   is
      type Class is
      limited record
         Elem : Test_Class_With_Namespace_Members.Foo.Bar.Class;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN3BazC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Baz;

end Test_Class_With_Namespace_Members.Root;
