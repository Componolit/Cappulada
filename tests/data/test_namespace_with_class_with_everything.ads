package Capdpa.With_Class.With_Everything
is
   One : constant := 1;
   Two : constant := 2;
   type Negative is (Minus_One, Minus_Two);
   for Negative use (Minus_One => -1, Minus_Two => -2);
   type Class is
   tagged limited record
      Public_Int : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   procedure Public_Function
   with Import, Convention => CPP, External_Name => "";
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Class.With_Everything;
