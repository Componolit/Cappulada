with Test_Class_With_Class_Type.With_Class;

package Test_Class_With_Class_Type
   with SPARK_Mode => On
is
   package Full
      with SPARK_Mode => On
   is
      type Class is
      limited record
         Value : Test_Class_With_Class_Type.With_Class.In_Namespace.Class;
         Value_Ptr : Test_Class_With_Class_Type.With_Class.In_Namespace.Class_Address;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN4FullC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Full;

end Test_Class_With_Class_Type;
