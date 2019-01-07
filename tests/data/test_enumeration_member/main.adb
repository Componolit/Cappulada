with System;
with Tests;
with Interfaces.C;
with Test_Enumeration_Member.Cls;

procedure Main
is
   use Test_Enumeration_Member;

   C1 : aliased Cls.Class  := Cls.Constructor;
   C2 : aliased Cls.Class  := Cls.Constructor (Cls.Elem2);
   Val1, Val2 : Cls.Elements;
   use type Cls.Elements;
begin
   Val1 := Cls.Get (C1'Access);
   Tests.Assert (Val1 = Cls.Invalid, "Wrong value returned (1): " & Val1'Img);

   Val2 := Cls.Get (C2'Access);
   Tests.Assert (Val2 = Cls.Elem2, "Wrong value returned (2): " & Val2'Img);
end Main;
