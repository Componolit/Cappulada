with Tests;
with Interfaces.C;
with Test_Static_Method.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Static_Method;
   use Interfaces.C;
   Value : Interfaces.C.int;
begin
   Value := Cls.Static_Method (15);
   Tests.Assert (Value = 57, "Wrong value returned:" & Value'Img);
end Main;
