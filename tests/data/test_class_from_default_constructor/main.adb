with Tests;
with Interfaces.C;
with Test_Class_From_Default_Constructor.Cls;

procedure Main
is
   use Test_Class_From_Default_Constructor;
   use Interfaces.C;
   Value : Interfaces.C.int;
   Class : aliased Cls.Class := Cls.Constructor;
begin
   Value := Cls.get_value (Class'Access);
   Tests.Assert (Value = 1234, "Wrong value returned:" & Value'Img);
end Main;
