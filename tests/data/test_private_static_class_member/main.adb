with Tests;
with Interfaces.C;
with Test_Private_Static_Class_Member.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Private_Static_Class_Member;

   C : Cls.Class := Cls.Constructor;
   V : short;
   use Interfaces.C;
begin
   Cls.Set (C, 34);
   V := Cls.Get (C);

   Tests.Assert (V = 34, "Wrong value returned: " & V'Img);
end Main;
