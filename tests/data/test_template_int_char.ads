package Capdpa.Container_T_Int_Char
is
   type Class is
   limited record
      A : aliased Capdpa.Int;
      B : aliased Capdpa.Char;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN9ContainerIicEC1Ev");
end Capdpa.Container_T_Int_Char;
