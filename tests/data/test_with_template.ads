with System;

package Capdpa.User
is
   type Class is
   limited record
      Cic : Container_T_Int_Char;
      Cii : Container_T_Int_Int;
      Cic2 : Container_T_Int_Char;
   end record
   with Import, Convention => CPP;
   type Class_Access is access Class;
   type Class_Address is new System.Address;
   type Class_Array is array (Long_Integer range <>) of Class;
   type Class_Access_Array is array (Long_Integer range <>) of Class_Access;
   type Class_Address_Array is array (Long_Integer range <>) of Class_Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.User;
