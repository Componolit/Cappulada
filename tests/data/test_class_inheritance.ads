with System;

package Capdpa.Inheritance
is
   type Inheritance_Private_Int is null record
      with Size => Capdpa.Int'Size;
   type Inheritance_Private_Void is null record
      with Size => Capdpa.Void_Address'Size;
   type Inheritance_Private_C_Float is null record
      with Size => Capdpa.C_Float'Size;
   type Class is
   limited record
      Public_Int : Capdpa.Int;
      Public_Pointer : Capdpa.Void_Address;
      Public_Float : Capdpa.C_Float;
      Private_Private_Int : Inheritance_Private_Int;
      Private_Private_Pointer : Inheritance_Private_Void;
      Private_Private_Float : Inheritance_Private_C_Float;
      Additional : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Access is access Class;
   type Class_Address is new System.Address;
   type Class_Array is array (Long_Integer range <>) of Class;
   type Class_Access_Array is array (Long_Integer range <>) of Class_Access;
   type Class_Address_Array is array (Long_Integer range <>) of Class_Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.Inheritance;
