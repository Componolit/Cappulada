package Capdpa.With_Members
is
   type Private_Int is limited private;
   type Private_Void is limited private;
   type Private_C_Float is limited private;

   type Class is
   limited record
      Public_Int : Capdpa.Int;
      Public_Pointer : Capdpa.Void_Address;
      Public_Float : Capdpa.C_Float;
      Private_Private_Int : Private_Int;
      Private_Private_Pointer : Private_Void;
      Private_Private_Float : Private_C_Float;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN12With_membersC1Ev");

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;
   type Private_Int is new Capdpa.Int;
   type Private_Void is new Capdpa.Void;
   type Private_C_Float is new Capdpa.C_Float;
end Capdpa.With_Members;
