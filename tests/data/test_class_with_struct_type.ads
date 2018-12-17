with System;

package Capdpa.With_Struct
is
   package Ws
   is
      type Class is
      limited record
         X : Capdpa.Int;
      end record
      with Import, Convention => CPP;
      type Class_Access is access Class;
      type Class_Address is new System.Address;
      type Class_Array is array (Long_Integer range <>) of Class;
      type Class_Access_Array is array (Long_Integer range <>) of Class_Access;
      type Class_Address_Array is array (Long_Integer range <>) of Class_Address;
      function Constructor return Class;
      pragma Cpp_Constructor (Constructor, "");
   end Ws;
   package Ws2 is
      type Class is null record;
      type Class_Address is new System.Address;
   end Ws2;
   type Class is
   limited record
      Value : Capdpa.With_Struct.Ws.Class;
      Value2 : Capdpa.With_Struct.Ws2.Class_Address;
   end record
   with Import, Convention => CPP;
   type Class_Access is access Class;
   type Class_Address is new System.Address;
   type Class_Array is array (Long_Integer range <>) of Class;
   type Class_Access_Array is array (Long_Integer range <>) of Class_Access;
   type Class_Address_Array is array (Long_Integer range <>) of Class_Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Struct;
