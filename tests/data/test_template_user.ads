with Capdpa.Container_T_Int_Char;
with Capdpa.Container_T_Int_Int;

package Capdpa.User
   with SPARK_Mode => On
is
   type Class is
   limited record
      Cic : Capdpa.Container_T_Int_Char.Class;
      Cii : Capdpa.Container_T_Int_Int.Class;
      Cic2 : Capdpa.Container_T_Int_Char.Class;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN4UserC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.User;
