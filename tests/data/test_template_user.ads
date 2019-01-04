
package Capdpa.User
is
   type Class is
   limited record
      Cic : Capdpa.Container_T_Int_Char;
      Cii : Capdpa.Container_T_Int_Int;
      Cic2 : Capdpa.Container_T_Int_Char;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN4UserC1Ev");
end Capdpa.User;
