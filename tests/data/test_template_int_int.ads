package Capdpa.Container_T_Int_Int
   with SPARK_Mode
is
   type Class is
   limited record
      A : Capdpa.Int;
      B : Capdpa.Int;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN9ContainerIiiEC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.Container_T_Int_Int;
