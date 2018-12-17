with System;

package Capdpa.Container_T_Int_Int
is
   type Class is
   limited record
      A : Capdpa.Int;
      B : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN19Container_T_int_intC1Ev");
end Capdpa.Container_T_Int_Int;
