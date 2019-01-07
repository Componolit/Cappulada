with Capdpa.Inheritance;

package Capdpa.Child
is
   type Class is
   limited record
      Inheritance : aliased Capdpa.Inheritance.Class;
      C : aliased Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN5ChildC1Ev");
end Capdpa.Child;
