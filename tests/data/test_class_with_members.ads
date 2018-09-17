with System;
package With_Members is
   type With_Members is
   tagged limited record
      Public_Int : Integer;
      Public_Pointer : System.Address;
      Public_Float : Float;
   end record
   with Import => CPP;
   function Constructor return With_Members;
   pragma Cpp_Constructor (Constructor, "");
end With_Members;
