with System;
with Tests;
with Interfaces.C;
with Test_Enumeration_Declaration;

procedure Main
is
   use Test_Enumeration_Declaration;

   C1 : Cls.Class  := Cls.Constructor;
   C2 : Cls.Class  := Cls.Constructor (Cls.Elem2);
   use type Cls.Elements;
begin
   Tests.Assert (C1.Member = Cls.Invalid, "Wrong value returned (1): " & C1.Member'Img);
   Tests.Assert (C2.Member = Cls.Elem2, "Wrong value returned (2): " & C2.Member'Img);
end Main;
