package Test_Namespace_With_Enum.With_Enum
   with SPARK_Mode => On
is
   type Weekend is (Saturday, Sunday)
   with Size => Test_Namespace_With_Enum.Unsigned_Int'Size;
   for Weekend use (Saturday => 0, Sunday => 1);
   type Constants is (One, Two, Three)
   with Size => Test_Namespace_With_Enum.Unsigned_Int'Size;
   for Constants use (One => 1, Two => 2, Three => 3);
end Test_Namespace_With_Enum.With_Enum;
