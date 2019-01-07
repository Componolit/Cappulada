with Capdpa.With_Members;

package Capdpa.Inheritance
is
   type Class is
   limited record
      With_Members : aliased Capdpa.With_Members.Class;
      Additional : aliased Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN11InheritanceC1Ev");
end Capdpa.Inheritance;
