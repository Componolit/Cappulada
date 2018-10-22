package Capdpa.User
is
   type Class is
   limited record
      Cic : Capdpa.Container_T_Int_Signed_Char;
      Cii : Capdpa.Container_T_Int_Int;
      Cic2 : Capdpa.Container_T_Int_Signed_Char;
   end record
   with Import, Convention => CPP;
   type Private_Class is limited null record
   with Size => Class'Size;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.User;
