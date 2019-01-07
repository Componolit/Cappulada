with Capdpa.With_Class.In_Namespace;

package Capdpa.Full
is
   type Class is
   limited record
      Value : aliased Capdpa.With_Class.In_Namespace.Class;
      Value_Ptr : aliased Capdpa.With_Class.In_Namespace.Class_Address;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN4FullC1Ev");
end Capdpa.Full;
