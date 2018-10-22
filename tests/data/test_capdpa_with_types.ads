package Capdpa
is
   subtype Uint8_T is Capdpa.Unsigned_Char;
   type Private_Uint8_T is limited null record
      with Size => Uint8_T'Size;
   subtype Int32_T is Capdpa.Int;
   type Private_Int32_T is limited null record
      with Size => Int32_T'Size;
   subtype U8 is Uint8_T;
   type Private_U8 is limited null record
      with Size => U8'Size;
end Capdpa;
