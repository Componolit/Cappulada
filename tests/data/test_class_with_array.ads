with System;

package Capdpa.With_Array
is
   type Int_Array is array (Integer range <>) of Capdpa.Int;
   type Class is
   limited record
      Car : Capdpa.With_Array.Int_Array(1 .. 5);
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Array;
