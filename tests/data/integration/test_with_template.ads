package Test_With_Template
   with SPARK_Mode => On
is
   package Container_T_Int_Char
      with SPARK_Mode => On
   is
      type Class is
      limited record
         A : Test_With_Template.Int;
         B : Test_With_Template.Char;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN9ContainerIicEC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Container_T_Int_Char;

   package Container_T_Int_Int
      with SPARK_Mode => On
   is
      type Class is
      limited record
         A : Test_With_Template.Int;
         B : Test_With_Template.Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN9ContainerIiiEC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Container_T_Int_Int;

   package User
      with SPARK_Mode => On
   is
      type Class is
      limited record
         Cic : Test_With_Template.Container_T_Int_Char.Class;
         Cii : Test_With_Template.Container_T_Int_Int.Class;
         Cic2 : Test_With_Template.Container_T_Int_Char.Class;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN4UserC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end User;

end Test_With_Template;
