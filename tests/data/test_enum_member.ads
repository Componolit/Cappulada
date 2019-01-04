package Capdpa.With_Enum
is
   type E_T is (A, B);
   for E_T use (A => 0, B => 1);
   type Class is
   limited record
      E : Capdpa.With_Enum.E_T;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN9With_EnumC1Ev");
end Capdpa.With_Enum;
