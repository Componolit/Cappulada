package Capdpa.With_Functions
is
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;
   type Private_Class is limited null record
   with Size => Class'Size;
   procedure Public_Function (Arg1 : Capdpa.Int)
   with Import, Convention => CPP, External_Name => "";
   function Named_Param (Param : Capdpa.Int) return Capdpa.Int
   with Import, Convention => CPP, External_Name => "";
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Functions;
