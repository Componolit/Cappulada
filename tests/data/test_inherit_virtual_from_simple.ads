package Capdpa.Simple
is
   pragma Warnings (Off, "* bits of ""Simple_Private_Int"" unused");
   type Simple_Private_Int is null record
      with Size => Capdpa.Int_Size;
   pragma Warnings (On, "* bits of ""Simple_Private_Int"" unused");
   pragma Warnings (Off, "* bits of ""Simple_Private_Void"" unused");
   type Simple_Private_Void is null record
      with Size => Capdpa.Void_Size;
   pragma Warnings (On, "* bits of ""Simple_Private_Void"" unused");
   pragma Warnings (Off, "* bits of ""Simple_Private_C_Float"" unused");
   type Simple_Private_C_Float is null record
      with Size => Capdpa.C_Float_Size;
   pragma Warnings (On, "* bits of ""Simple_Private_C_Float"" unused");
   type Class is
   tagged limited record
      Public_Int : Capdpa.Int;
      Public_Pointer : Capdpa.Void_Address;
      Public_Float : Capdpa.C_Float;
      Private_Private_Int : Simple_Private_Int;
      Private_Private_Pointer : Simple_Private_Void;
      Private_Private_Float : Simple_Private_C_Float;
      Additional : Capdpa.Int;
      S : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN6SimpleC1Ev");
   procedure Foo (This : access Class)
   with Import, Convention => CPP, External_Name => "_ZN6Simple3fooEv";
end Capdpa.Simple;
