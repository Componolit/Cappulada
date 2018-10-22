package Capdpa.Container_T_Int_Signed_Char
is
   type Class is
   limited record
      A : Capdpa.Int;
      B : Capdpa.Signed_Char;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Container_T_Int_Signed_Char;
