package Test_Class_With_Static_Functions
   with SPARK_Mode => On
is
   package With_Functions
      with SPARK_Mode => On
   is
      type Class is
      limited record
         null;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      procedure Public_Function (This : Class; Arg1 : Test_Class_With_Static_Functions.Int)
      with Global => null, Import, Convention => CPP, External_Name => "_ZN14With_functions15public_functionEi";

      function Static_Function (Arg1 : Test_Class_With_Static_Functions.Char) return Test_Class_With_Static_Functions.Int
      with Global => null, Import, Convention => CPP, External_Name => "_ZN14With_functions15static_functionEc";

      function Named_Param (This : Class; Param : Test_Class_With_Static_Functions.Int) return Test_Class_With_Static_Functions.Int
      with Global => null, Import, Convention => CPP, External_Name => "_ZN14With_functions11named_paramEi";

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN14With_functionsC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end With_Functions;

end Test_Class_With_Static_Functions;
