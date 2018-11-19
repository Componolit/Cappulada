package Capdpa.With_Typedef.Use_Type
is
   type Class is
   limited record
      C : U8;
      I : I32;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Typedef.Use_Type;
