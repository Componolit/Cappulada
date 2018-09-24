with System;
package Capdpa.With_Members
is
   type Class is
   tagged limited record
      Public_Int : Integer;
      Public_Pointer : System.Address;
      Public_Float : Float;
   end record
   with Import => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Members;
