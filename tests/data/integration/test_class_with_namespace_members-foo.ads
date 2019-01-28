package Test_Class_With_Namespace_Members.Foo
   with SPARK_Mode => On
is
   package Bar
      with SPARK_Mode => On
   is
      type Class is
      limited record
         null;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN3Foo3BarC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Bar;

end Test_Class_With_Namespace_Members.Foo;
