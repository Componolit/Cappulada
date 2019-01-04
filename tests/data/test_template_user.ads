with Capdpa.Container_T_Int_Char;
with Capdpa.Container_T_Int_Int;

package Capdpa.User
is
   type Class is
   limited record
      Cic : Capdpa.Container_T_Int_Char.Class;
      Cii : Capdpa.Container_T_Int_Int.Class;
      Cic2 : Capdpa.Container_T_Int_Char.Class;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN4UserC1Ev");
end Capdpa.User;
