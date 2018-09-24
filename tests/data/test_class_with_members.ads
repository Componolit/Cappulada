with System;
package With_Members
is
   type Class is
   tagged limited record
      Public_Int : Integer;
      Public_Pointer : System.Address;
      Public_Float : Float;
   end record
   with Import => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end With_Members;
