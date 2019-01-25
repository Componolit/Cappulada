package Test_Inherit_Virtual_From_Simple
   with SPARK_Mode => On
is
   package With_Members
      with SPARK_Mode => On
   is
      type Private_Int is limited private;
      type Private_Int_Address is limited private;
      type Private_Void is limited private;
      type Private_Void_Address is limited private;
      type Private_C_Float is limited private;
      type Private_C_Float_Address is limited private;

      type Class is
      limited record
         Public_Int : Test_Inherit_Virtual_From_Simple.Int;
         Public_Pointer : Test_Inherit_Virtual_From_Simple.Void_Address;
         Public_Float : Test_Inherit_Virtual_From_Simple.C_Float;
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
      type Private_Int is new Test_Inherit_Virtual_From_Simple.Int;
      type Private_Int_Address is access Private_Int;
      type Private_Void is new Test_Inherit_Virtual_From_Simple.Void;
      type Private_Void_Address is access Private_Void;
      type Private_C_Float is new Test_Inherit_Virtual_From_Simple.C_Float;
      type Private_C_Float_Address is access Private_C_Float;
   end With_Members;

   package Inheritance
      with SPARK_Mode => On
   is
      type Class is
      limited record
         With_Members : Test_Inherit_Virtual_From_Simple.With_Members.Class;
         Additional : Test_Inherit_Virtual_From_Simple.Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN11InheritanceC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Inheritance;

   package Simple
      with SPARK_Mode => On
   is
      type Class is
      tagged limited record
         Inheritance : Test_Inherit_Virtual_From_Simple.Inheritance.Class;
         S : Test_Inherit_Virtual_From_Simple.Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN6SimpleC1Ev");

      procedure Foo (This : Class)
      with Global => null, Import, Convention => CPP, External_Name => "_ZN6Simple3fooEv";

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Simple;

end Test_Inherit_Virtual_From_Simple;
