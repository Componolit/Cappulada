package Capdpa.With_Array
   with SPARK_Mode => On
is
   type Int_Array is array (Integer range <>) of Capdpa.Int;

   type Class is
   limited record
      Car : Capdpa.With_Array.Int_Array (1 .. 5);
   end record
   with Import, Convention => CPP;

   type Class_Address is limited private;

   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");

private
   type Class_Address is access Class;

end Capdpa.With_Array;
