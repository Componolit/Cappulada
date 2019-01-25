with System;
with Tests;
with Interfaces.C;
with Test_Enumeration_Values;
with Ada.Unchecked_Conversion;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Enumeration_Values;

   C1 : Cls.Class  := Cls.Constructor;
   C2 : Cls.Class  := Cls.Constructor (Elem2);
   Val1, Val2 : Elements;
   use type Elements;

   type Enum_Val is mod 2 ** Elements'Size;
   V : Enum_Val;
   function To_Val is new Ada.Unchecked_Conversion (Elements, Enum_Val);
begin
   Val1 := Cls.Get (C1);
   Tests.Assert (Val1'Valid, "Enum value not valid (1)");
   Tests.Assert (Val1 = Invalid, "Wrong value returned (1): " & Val1'Img);

   Val2 := Cls.Get (C2);
   Tests.Assert (Val2'Valid, "Enum value not valid (2)");
   Tests.Assert (Val2 = Elem2, "Wrong value returned (2): " & Val2'Img);

   V := To_Val (Negative);
   Tests.Assert (V = -5000, "Invalid enum value (0): " & V'Img);

   V := To_Val (Invalid);
   Tests.Assert (V = 17, "Invalid enum value (1): " & V'Img);

   V := To_Val (Elem1);
   Tests.Assert (V = 119, "Invalid enum value (2): " & V'Img);

   V := To_Val (Elem2);
   Tests.Assert (V = 5, "Invalid enum value (3): " & V'Img);

   V := To_Val (Elem3);
   Tests.Assert (V = 1, "Invalid enum value (4): " & V'Img);

   V := To_Val (Big);
   Tests.Assert (V = 2**32-1, "Invalid enum value (5): " & V'Img);
end Main;
