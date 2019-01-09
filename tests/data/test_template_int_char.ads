package Capdpa.Container_T_Int_Char
is
   type Class is
   limited record
      A : Capdpa.Int;
      B : Capdpa.Char;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN9ContainerIicEC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.Container_T_Int_Char;
