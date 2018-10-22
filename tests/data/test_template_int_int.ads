package Capdpa.Container_T_Int_Int
is
   type Class is
   limited record
      A : Capdpa.Int;
      B : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Private_Class is limited null record
   with Size => Class'Size;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Container_T_Int_Int;
