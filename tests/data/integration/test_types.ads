package Test_Types
   with SPARK_Mode => On
is
   subtype Uint8_T is Test_Types.Unsigned_Char;
   subtype Int32_T is Test_Types.Int;
   subtype U8 is Uint8_T;
   subtype Ull is Test_Types.Unsigned_Long_Long;
end Test_Types;
