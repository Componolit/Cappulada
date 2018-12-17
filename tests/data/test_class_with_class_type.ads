with Capdpa.With_Class.In_Namespace;
with System;

package Capdpa.Full
is
   type Class is
   limited record
      Value : Capdpa.With_Class.In_Namespace.Class;
      Value_Ptr : Capdpa.With_Class.In_Namespace.Class_Address;
   end record
   with Import, Convention => CPP;
   type Class_Access is access Class;
   type Class_Address is new System.Address;
   type Class_Array is array (Long_Integer range <>) of Class;
   type Class_Access_Array is array (Long_Integer range <>) of Class_Access;
   type Class_Address_Array is array (Long_Integer range <>) of Class_Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Full;
