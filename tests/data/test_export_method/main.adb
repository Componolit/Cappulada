with Tests;
with Interfaces.C;
with Test_Export_Method;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Export_Method;

   I : Cls.Class := Cls.Constructor (11);
   Val1, Val2 : int;

   use Interfaces.C;
begin
   Val1 := Cls.Ada_Method (I, 5);
   Tests.Assert (Val1 = 16, "Wrong value returned (1): " & Val1'Img);

   Val2 := Cls.Cpp_Method (I, 7);
   Tests.Assert (Val2 = 25, "Wrong value returned (2): " & Val2'Img);
end Main;
