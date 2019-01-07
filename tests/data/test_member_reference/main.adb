with System;
with Tests;
with Interfaces.C;
with Test_Member_Reference.Cls;

procedure Main
is
   use Test_Member_Reference;

   C1 : aliased Cls.Class  := Cls.Constructor;
   C2 : aliased Cls.Class  := Cls.Constructor (518);
   Val1, Val2 : Int;
   use Interfaces.C;
begin
   Val1 := Cls.Method (C1'Access);
   Tests.Assert (Val1 = 17, "Wrong value returned (1): " & Val1'Img);
   Tests.Assert (C1.Ref.all = 16, "Wrong value returned (2): " & C1.Ref.all'Img);

   Val2 := Cls.Method (C2'Access);
   Tests.Assert (Val2 = 519, "Wrong value returned (3): " & Val2'Img);
   Tests.Assert (C2.Ref.all = 518, "Wrong value returned (4): " & C2.Ref.all'Img);
end Main;
