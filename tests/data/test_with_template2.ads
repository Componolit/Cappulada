package Capdpa.Container_T_Int_Int
is
   type Class is
   limited record
      A : Capdpa.Int;
      B : Capdpa.Char;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Container_T_Int_Int;

