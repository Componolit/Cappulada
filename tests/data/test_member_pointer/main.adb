with System;
with Tests;
with Interfaces.C;
with Test_Member_Pointer;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Member_Pointer;

   V : int := 123456;
   C : aliased Cls.Class  := Cls.Constructor(V);
   Val1 : Int;
   use Interfaces.C;
begin
   Val1 := Cls.Method (C);
   Tests.Assert (Val1 = V + 1, "Wrong value returned (1): " & Val1'Img);
end Main;
