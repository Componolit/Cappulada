package Capdpa.With_Class.With_Everything
is
   One : constant := 1;
   Two : constant := 2;
   type Negative is (Minus_Two, Minus_One);
   for Negative use (Minus_Two => -2, Minus_One => -1);
   pragma Warnings (Off, "* bits of ""With_Everything_Private_Int"" unused");
   type With_Everything_Private_Int is null record
      with Size => Capdpa.Int_Size;
   pragma Warnings (On, "* bits of ""With_Everything_Private_Int"" unused");
   type Class is
   limited record
      Private_Private_Int : aliased With_Everything_Private_Int;
      Public_Int : aliased Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   procedure Public_Function (This : access Class)
   with Import, Convention => CPP, External_Name => "_ZN10With_class15With_everything15public_functionEv";
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN10With_class15With_everythingC1Ev");
end Capdpa.With_Class.With_Everything;
