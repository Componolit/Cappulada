package Capdpa.User
   with SPARK_Mode => On
is
   type Class is
   limited record
      Cic : aliased Container_T_Int_Char;
      Cii : aliased Container_T_Int_Int;
      Cic2 : aliased Container_T_Int_Char;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.User;
