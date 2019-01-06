package Capdpa.With_Members
is
   pragma Warnings (Off, "* bits of ""With_Members_Private_Int"" unused");
   type With_Members_Private_Int is null record
      with Size => Capdpa.Int_Size;
   pragma Warnings (On, "* bits of ""With_Members_Private_Int"" unused");
   pragma Warnings (Off, "* bits of ""With_Members_Private_Void"" unused");
   type With_Members_Private_Void is null record
      with Size => Capdpa.Void_Size;
   pragma Warnings (On, "* bits of ""With_Members_Private_Void"" unused");
   pragma Warnings (Off, "* bits of ""With_Members_Private_C_Float"" unused");
   type With_Members_Private_C_Float is null record
      with Size => Capdpa.C_Float_Size;
   pragma Warnings (On, "* bits of ""With_Members_Private_C_Float"" unused");
   type Class is
   limited record
      Public_Int : Capdpa.Int;
      Public_Pointer : Capdpa.Void_Address;
      Public_Float : Capdpa.C_Float;
      Private_Private_Int : With_Members_Private_Int;
      Private_Private_Pointer : With_Members_Private_Void;
      Private_Private_Float : With_Members_Private_C_Float;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN12With_membersC1Ev");
end Capdpa.With_Members;
