with Capdpa.With_Virtual;

package Capdpa.From_Virtual
   with SPARK_Mode => On
is
   type Class is new Capdpa.With_Virtual.Class with
   record
      V : Capdpa.Int;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN12From_VirtualC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.From_Virtual;
