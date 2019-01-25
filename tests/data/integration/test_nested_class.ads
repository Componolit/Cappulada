package Test_Nested_Class
   with SPARK_Mode => On
is
   package Outer
      with SPARK_Mode => On
   is
      package Inner
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
         pragma Cpp_Constructor (Constructor, "_ZN5Outer5InnerC1Ev");

      private
         pragma SPARK_Mode (Off);

         type Class_Address is access Class;

      end Inner;
      type Class is
      limited record
         I : Test_Nested_Class.Outer.Inner.Class;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN5OuterC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Outer;

end Test_Nested_Class;
