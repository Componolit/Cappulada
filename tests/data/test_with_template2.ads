package Capdpa.Container_T_Int_Int
   with SPARK_Mode => On
is
   type Class is
   limited record
      A : aliased Capdpa.Int;
      B : aliased Capdpa.Char;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Container_T_Int_Int;

