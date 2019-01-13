package Capdpa.With_Enum
   with SPARK_Mode => On
is
   type Weekend is (Saturday, Sunday)
   with Size => Capdpa.Unsigned_Int'Size;
   for Weekend use (Saturday => 0, Sunday => 1);
   type Constants is (One, Two, Three)
   with Size => Capdpa.Unsigned_Int'Size;
   for Constants use (One => 1, Two => 2, Three => 3);
end Capdpa.With_Enum;
