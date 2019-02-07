package Test_Inherit_From_Virtual
   with SPARK_Mode => On
is
   package With_Virtual
      with SPARK_Mode => On
   is
      type Class is
      tagged limited record
         null;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN12With_VirtualC1Ev");

      procedure Foo (This : Class)
      with Global => null, Import, Convention => CPP, External_Name => "_ZN12With_Virtual3fooEv";

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end With_Virtual;

   package From_Virtual
      with SPARK_Mode => On
   is
      type Class is new Test_Inherit_From_Virtual.With_Virtual.Class with
      record
         V : Test_Inherit_From_Virtual.Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN12From_VirtualC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end From_Virtual;

end Test_Inherit_From_Virtual;
