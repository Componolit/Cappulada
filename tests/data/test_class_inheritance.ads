with Capdpa.With_Members;

package Capdpa.Inheritance
   with SPARK_Mode
is
   type Class is
   limited record
      With_Members : Capdpa.With_Members.Class;
      Additional : Capdpa.Int;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN11InheritanceC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.Inheritance;
