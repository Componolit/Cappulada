with System;
with Tests;
with Interfaces.C;
with Test_Enumeration_Custom_Base_Type.Cls;
with Ada.Unchecked_Conversion;

procedure Main
is
   use Test_Enumeration_Custom_Base_Type;
   use type Interfaces.C.unsigned_char;
   use type Cls.Values3;
   function To_Val is new Ada.Unchecked_Conversion (Cls.Values3, unsigned_char);
begin
   Tests.Assert (Cls.Values'Size = 32, "Wrong size for int-based type: " & Cls.Values'Size'Img);
   Tests.Assert (Cls.Values2'Size = 32, "Wrong value for default enum type: " & Cls.Values2'Size'Img);
   Tests.Assert (Cls.Values3'Size = 8, "Wrong value for char-based enum type: " & Cls.Values3'Size'Img);
   Tests.Assert (To_Val (Cls.Val9) = 255, "Wrong value for enum element:  " & To_Val (Cls.Val9)'Img);
end Main;
