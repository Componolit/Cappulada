with System;
with Tests;
with Interfaces.C;
with Test_Enumeration_Class;

procedure Main
is
   use Test_Enumeration_Class;

   C1 : Cls.Class  := Cls.Constructor;
   C2 : Cls.Class  := Cls.Constructor (Cls.Elem2);
   use type Cls.Elements1;
   use type Cls.Elements2;
begin
   Tests.Assert (C1.Member1 = Cls.Invalid, "Wrong value returned (1): " & C1.Member1'Img);
   Tests.Assert (C2.Member1 = Cls.Elem2, "Wrong value returned (2): " & C2.Member1'Img);
   Tests.Assert (C1.Member2 = Cls.Invalid, "Wrong value returned (3): " & C1.Member2'Img);
   Tests.Assert (C2.Member2 = Cls.Invalid, "Wrong value returned (4): " & C2.Member2'Img);
end Main;
