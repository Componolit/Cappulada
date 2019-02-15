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
   subtype Int8_T is Test_Types.Char;
   subtype Int8_T_Array is Test_Types.Char_Array;
   subtype Int16_T is Test_Types.Short;
   subtype Int16_T_Array is Test_Types.Short_Array;
   subtype Iuarray is Test_Types.Int_Array;
   subtype Icarray is Test_Types.Int_Array (1 .. 10);
end Test_Types;
