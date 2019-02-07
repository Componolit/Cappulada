package Test_Class_With_Arrays
   with SPARK_Mode => On
is
   package Wa
      with SPARK_Mode => On
   is
      type Private_Int is limited private;
      type Private_Int_Address is limited private;
      type Private_Int_Array is array (Natural range <>) of Private_Int;
      type Private_Int_Address_Array is array (Natural range <>) of Private_Int_Address;

      type Class is
      limited record
         Private_Px : Private_Int_Array (1 .. 42);
         Name : Test_Class_With_Arrays.Unsigned_Int_Array (1 .. 42);
         Argv : Test_Class_With_Arrays.Char_Address_Array (1 .. 5);
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN2WaC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;
      type Private_Int is new Test_Class_With_Arrays.Int;
      type Private_Int_Address is access Private_Int;
   end Wa;

end Test_Class_With_Arrays;
