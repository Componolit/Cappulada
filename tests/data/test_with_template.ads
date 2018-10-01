package Capdpa.User
is
   type Class is
   tagged limited record
      Cic : Container_T_Int_Char;
      Cii : Container_T_Int_Int;
      Cic2 : Container_T_Int_Char;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.User;
