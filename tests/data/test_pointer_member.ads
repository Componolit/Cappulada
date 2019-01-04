package Capdpa.With_Pointer
is
   type Class is
   limited record
      P : Capdpa.Int_Address;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN12With_PointerC1Ev");
end Capdpa.With_Pointer;
