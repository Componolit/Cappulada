package Capdpa.Inheritance
is
   type Class is
   type Class is
   limited record
      Public_Int : Capdpa.Int;
      Public_Pointer : Capdpa.C_Address;
      Public_Float : Capdpa.C_Float;
      Private_Private_Int : Capdpa.Private_Int;
      Private_Private_Pointer : Capdpa.Private_C_Address;
      Private_Private_Float : Capdpa.Private_C_Float;
      Additional : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Private_Class is limited null record
   with Size => Class'Size;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Inheritance;
