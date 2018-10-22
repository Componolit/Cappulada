with System;

package Capdpa.With_Members
is
   type Class is
   limited record
      Public_Int : Capdpa.Int;
      Public_Pointer : System.Address;
      Public_Float : Capdpa.C_Float;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Members;
