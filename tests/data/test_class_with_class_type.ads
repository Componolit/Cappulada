with Capdpa.With_Class.In_Namespace;

package Capdpa.Full
is
   type Class is
   tagged limited record
      Value : Capdpa.With_Class.In_Namespace.Class;
      Value_Ptr : access Capdpa.With_Class.In_Namespace.Class;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Full;
