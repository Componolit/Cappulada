with System;

package Capdpa.With_Reference
is
   type Class is
   limited record
      R : access Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Reference;