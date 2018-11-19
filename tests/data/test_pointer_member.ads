with System;

package Capdpa.With_Pointer
is
   type Class is
   limited record
      P : Capdpa.Int_Address;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Pointer;
