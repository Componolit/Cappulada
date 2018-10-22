with Capdpa.With_Class.In_Namespace;

package Capdpa.Full
is
   type Class is
   limited record
      Value : Capdpa.With_Class.In_Namespace.Class;
      Value_Ptr : access Capdpa.With_Class.In_Namespace.Class;
   end record
   with Import, Convention => CPP;
   type Private_Class is limited null record
   with Size => Class'Size;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Full;
