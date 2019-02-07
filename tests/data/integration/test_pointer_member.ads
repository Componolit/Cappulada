package Test_Pointer_Member
   with SPARK_Mode => On
is
   package With_Pointer
      with SPARK_Mode => On
   is
      type Class is
      limited record
         P : Test_Pointer_Member.Int_Address;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN12With_PointerC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end With_Pointer;

end Test_Pointer_Member;
