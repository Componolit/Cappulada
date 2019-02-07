package Test_Types
   with SPARK_Mode => On
is
   subtype Uint8_T is Test_Types.Unsigned_Char;
   subtype Uint8_T_Array is Test_Types.Unsigned_Char_Array;
   subtype Int32_T is Test_Types.Int;
   subtype Int32_T_Array is Test_Types.Int_Array;
   subtype U8 is Uint8_T;
   subtype U8_Array is Uint8_T_Array;
   subtype Ull is Test_Types.Unsigned_Long_Long;
   subtype Ull_Array is Test_Types.Unsigned_Long_Long_Array;
end Test_Types;
