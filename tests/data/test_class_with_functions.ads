package Capdpa.With_Functions
is
   type Class is
   tagged limited record
      null;
   end record
   with Import, Convention => CPP;
   procedure Public_Function (Arg1 : Integer);
   with Import, Convention => CPP, External_Name => "";
   function Named_Param (Param : Integer) return Integer
   with Import, Convention => CPP, External_Name => "";
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Functions;
