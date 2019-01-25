package Test_Namespace_With_Typedef.With_Typedef
   with SPARK_Mode => On
is
   subtype U8 is Test_Namespace_With_Typedef.Unsigned_Char;
   subtype I32 is Test_Namespace_With_Typedef.Int;
end Test_Namespace_With_Typedef.With_Typedef;
