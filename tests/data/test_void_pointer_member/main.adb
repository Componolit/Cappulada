with System;
with Tests;
with Interfaces.C;
with Test_Void_Pointer_Member.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use type System.Address;
   use Test_Void_Pointer_Member;
   Inst : aliased Cls.Class := Cls.Constructor (System'To_Address (1234567));
begin
   Tests.Assert (Cls.Get (Inst) = System'To_Address (1234567), "Wrong value returned (1): ");
end Main;
