with Capdpa.Inheritance;

package Capdpa.Simple
   with SPARK_Mode
is
   type Class is
   tagged limited record
      Inheritance : Capdpa.Inheritance.Class;
      S : Capdpa.Int;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN6SimpleC1Ev");

   procedure Foo (This : Class)
   with Global => null, Import, Convention => CPP, External_Name => "_ZN6Simple3fooEv";

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.Simple;
