package Test_Namespace_With_Typedef_With_Class.With_Typedef
   with SPARK_Mode => On
is
   subtype U8 is Test_Namespace_With_Typedef_With_Class.Unsigned_Char;
   subtype U8_Array is Test_Namespace_With_Typedef_With_Class.Unsigned_Char_Array;
   subtype I32 is Test_Namespace_With_Typedef_With_Class.Int;
   subtype I32_Array is Test_Namespace_With_Typedef_With_Class.Int_Array;
   package Use_Type
      with SPARK_Mode => On
   is
      type Class is
      limited record
         C : U8;
         I : I32;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;
      type Class_Array is array (Natural range <>) of Class;
      type Class_Address_Array is array (Natural range <>) of Class_Address;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN12With_typedef8Use_typeC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Use_Type;

end Test_Namespace_With_Typedef_With_Class.With_Typedef;
