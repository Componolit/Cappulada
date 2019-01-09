with Tests;
with Interfaces.C;
with Test_Class_From_Custom_Constructor.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Class_From_Custom_Constructor;
   use Interfaces.C;
   Value : Interfaces.C.int;
   D     : constant Interfaces.C.int := 78910;
   Class : aliased Cls.Class := Cls.Constructor (D);
begin
   Value := Cls.get_value (Class);
   Tests.Assert (Value = 1234 + D, "Wrong value returned:" & Value'Img);
end Main;
