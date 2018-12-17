with System;

package Capdpa.With_Functions
is
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   procedure Public_Function (Arg1 : Capdpa.Int)
   with Import, Convention => CPP, External_Name => "_ZN14With_functions15public_functionEi";
   function Named_Param (Param : Capdpa.Int) return Capdpa.Int
   with Import, Convention => CPP, External_Name => "_ZN14With_functions11named_paramEi";
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN14With_functionsC1Ev");
end Capdpa.With_Functions;
