package Capdpa.With_Class.With_Everything
   with SPARK_Mode
is
   One : constant := 1;
   Two : constant := 2;
   type Negative is (Minus_Two, Minus_One)
   with Size => Capdpa.Int'Size;
   for Negative use (Minus_Two => -2, Minus_One => -1);
   type Private_Int is limited private;

   type Class is
   limited record
      Private_Private_Int : Private_Int;
      Public_Int : Capdpa.Int;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   procedure Public_Function (This : Class)
   with Global => null, Import, Convention => CPP, External_Name => "_ZN10With_class15With_everything15public_functionEv";

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN10With_class15With_everythingC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;
   type Private_Int is new Capdpa.Int;
end Capdpa.With_Class.With_Everything;
