package Capdpa.Container_T_Int_Char
   with SPARK_Mode
is
   type Class is
   limited record
      A : Capdpa.Int;
      B : Capdpa.Char;
   end record
   with Import, Convention => CPP;

   type Class_Address is limited private;

   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.Container_T_Int_Char;
