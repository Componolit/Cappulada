with Capdpa.Inheritance;

package Capdpa.Simple
is
   type Class is
   tagged limited record
      Inheritance : aliased Capdpa.Inheritance.Class;
      S : aliased Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN6SimpleC1Ev");
   procedure Foo (This : access Class)
   with Import, Convention => CPP, External_Name => "_ZN6Simple3fooEv";
end Capdpa.Simple;
