with System;

package Capdpa.With_Functions
is
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;
   type Class_Access is access Class;
   type Class_Address is new System.Address;
   type Class_Array is array (Long_Integer range <>) of Class;
   type Class_Access_Array is array (Long_Integer range <>) of Class_Access;
   type Class_Address_Array is array (Long_Integer range <>) of Class_Address;
   procedure Public_Function (Arg1 : Capdpa.Int)
   with Import, Convention => CPP, External_Name => "";
   function Named_Param (Param : Capdpa.Int) return Capdpa.Int
   with Import, Convention => CPP, External_Name => "";
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Functions;
