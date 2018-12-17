with System;

package Capdpa.With_Constants
is
   One : constant := 1;
   Two : constant := 2;
   Three : constant := 3;
   type Negative is (Minus_One, Minus_Two, Minus_Three);
   for Negative use (Minus_One => -1, Minus_Two => -2, Minus_Three => -3);
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;
   type Class_Access is access Class;
   type Class_Address is new System.Address;
   type Class_Array is array (Long_Integer range <>) of Class;
   type Class_Access_Array is array (Long_Integer range <>) of Class_Access;
   type Class_Address_Array is array (Long_Integer range <>) of Class_Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Constants;
