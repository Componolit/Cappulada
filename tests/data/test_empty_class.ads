with System;

package Capdpa.Empty
is
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Empty;
