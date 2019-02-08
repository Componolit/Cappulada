with Tests;
with Interfaces.C;
with Test_Nested_Private_Class;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Nested_Private_Class;
   use Interfaces.C;
   O : Outer.Class := Outer.Constructor;
begin
   Tests.Assert (O.O = 42, "Wrong value returned: " & O.O'Img);
end Main;
