package Test_Enum_Member
   with SPARK_Mode => On
is
   package With_Enum
      with SPARK_Mode => On
   is
      type E_T is (A, B)
      with Size => Test_Enum_Member.Unsigned_Int'Size;
      for E_T use (A => 0, B => 1);
      type Class is
      limited record
         E : Test_Enum_Member.With_Enum.E_T;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN9With_EnumC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end With_Enum;

end Test_Enum_Member;
