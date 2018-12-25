with Tests;
with Interfaces.C;
with Test_Namespace_With_Class.Outer.Cls;

procedure Main
is
   use Test_Namespace_With_Class;
   use Interfaces.C;
   Value : Interfaces.C.int;
   Class : aliased Outer.Cls.Class := Outer.Cls.Constructor;
begin
   Value := Outer.Cls.get_value (Class'Access);
   Tests.Assert (Value = 1234, "Wrong value returned:" & Value'Img);
end Main;
