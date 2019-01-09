package Capdpa.With_Constants
is
   One : constant := 1;
   Two : constant := 2;
   Three : constant := 3;
   type Negative is (Minus_Three, Minus_Two, Minus_One);
   for Negative use (Minus_Three => -3, Minus_Two => -2, Minus_One => -1);
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN14With_constantsC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.With_Constants;
