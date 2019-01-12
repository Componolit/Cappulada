with Capdpa.Inheritance;

package Capdpa.Child
   with SPARK_Mode
is
   type Class is
   limited record
      Inheritance : Capdpa.Inheritance.Class;
      C : Capdpa.Int;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN5ChildC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.Child;
