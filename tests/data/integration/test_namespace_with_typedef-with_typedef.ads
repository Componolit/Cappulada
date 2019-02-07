package Test_Namespace_With_Typedef.With_Typedef
   with SPARK_Mode => On
is
   subtype U8 is Test_Namespace_With_Typedef.Unsigned_Char;
   subtype U8_Array is Test_Namespace_With_Typedef.Unsigned_Char_Array;
   subtype I32 is Test_Namespace_With_Typedef.Int;
   subtype I32_Array is Test_Namespace_With_Typedef.Int_Array;
end Test_Namespace_With_Typedef.With_Typedef;
