package Capdpa.Simple
is
   type Simple_Private_Int is null record
      with Size => Capdpa.Int'Size;
   type Simple_Private_C_Address is null record
      with Size => Capdpa.C_Address'Size;
   type Simple_Private_C_Float is null record
      with Size => Capdpa.C_Float'Size;
   type Class is
   tagged limited record
      Public_Int : Capdpa.Int;
      Public_Pointer : Capdpa.C_Address;
      Public_Float : Capdpa.C_Float;
      Private_Private_Int : Simple_Private_Int;
      Private_Private_Pointer : Simple_Private_C_Address;
      Private_Private_Float : Simple_Private_C_Float;
      Additional : Capdpa.Int;
      S : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
   procedure Foo
   with Import, Convention => CPP, External_Name => "";
end Capdpa.Simple;
