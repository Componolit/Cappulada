with Capdpa.With_Class.In_Namespace;

package Capdpa.Full
is
   type Class is
   limited record
      Value : Capdpa.With_Class.In_Namespace.Class;
      Value_Ptr : Capdpa.With_Class.In_Namespace.Class_Address;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN4FullC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Capdpa.Full;
