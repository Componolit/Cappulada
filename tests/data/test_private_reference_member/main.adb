with Tests;
with Interfaces.C;
with Test_Private_Reference_Member;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Private_Reference_Member;
   C1 : Privref.Class := Privref.Constructor (100);
   C2 : Privref.Class := Privref.Constructor;
   Val1, Val2 : int;
   use Interfaces.C;
begin
   Val1 := Privref.Get (C1);
   Tests.Assert (Val1 = 100, "Wrong value returned (1): " & Val1'Img);
   Val2 := Privref.Get (C2);
   Tests.Assert (Val2 = 42, "Wrong value returned (2): " & Val2'Img);
end Main;
