with System;

package Capdpa.With_Reference
is
   type Class is
   limited record
      R : access Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN14With_ReferenceC1Ev");
end Capdpa.With_Reference;
