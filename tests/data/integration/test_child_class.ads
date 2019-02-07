package Test_Child_Class
   with SPARK_Mode => On
is
   package With_Members
      with SPARK_Mode => On
   is
      type Private_Int is limited private;
      type Private_Int_Address is limited private;
      type Private_Int_Array is array (Natural range <>) of Private_Int;
      type Private_Int_Address_Array is array (Natural range <>) of Private_Int_Address;
      type Private_Void is limited private;
      type Private_Void_Address is limited private;
      type Private_Void_Array is array (Natural range <>) of Private_Void;
      type Private_Void_Address_Array is array (Natural range <>) of Private_Void_Address;
      type Private_C_Float is limited private;
      type Private_C_Float_Address is limited private;
      type Private_C_Float_Array is array (Natural range <>) of Private_C_Float;
      type Private_C_Float_Address_Array is array (Natural range <>) of Private_C_Float_Address;

      type Class is
      limited record
         Public_Int : Test_Child_Class.Int;
         Public_Pointer : Test_Child_Class.Void_Address;
         Public_Float : Test_Child_Class.C_Float;
         Private_Private_Int : Private_Int;
         Private_Private_Pointer : Private_Void;
         Private_Private_Float : Private_C_Float;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN12With_membersC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;
      type Private_Int is new Test_Child_Class.Int;
      type Private_Int_Address is access Private_Int;
      type Private_Void is new Test_Child_Class.Void;
      type Private_Void_Address is access Private_Void;
      type Private_C_Float is new Test_Child_Class.C_Float;
      type Private_C_Float_Address is access Private_C_Float;
   end With_Members;

   package Inheritance
      with SPARK_Mode => On
   is
      type Class is
      limited record
         With_Members : Test_Child_Class.With_Members.Class;
         Additional : Test_Child_Class.Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN11InheritanceC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Inheritance;

   package Child
      with SPARK_Mode => On
   is
      type Class is
      limited record
         Inheritance : Test_Child_Class.Inheritance.Class;
         C : Test_Child_Class.Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN5ChildC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Child;

end Test_Child_Class;
