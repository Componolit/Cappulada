package Capdpa.With_Pointer
   with SPARK_Mode
is
   type Class is
   limited record
      P : Capdpa.Int_Address;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN12With_PointerC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.With_Pointer;
