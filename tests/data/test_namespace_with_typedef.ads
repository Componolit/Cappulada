package Capdpa.With_Typedef
is
   subtype U8 is Capdpa.Unsigned_Char;
   type Private_U8 is limited null record
      with Size => U8'Size;
   subtype I32 is Capdpa.Int;
   type Private_I32 is limited null record
      with Size => I32'Size;
end Capdpa.With_Typedef;
