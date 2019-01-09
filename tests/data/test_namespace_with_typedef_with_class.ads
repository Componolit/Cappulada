package Capdpa.With_Typedef.Use_Type
is
   type Class is
   limited record
      C : U8;
      I : I32;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN12With_typedef8Use_typeC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.With_Typedef.Use_Type;
