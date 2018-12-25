with Tests;
with Interfaces.C;
with Test_Multiple_Custom_Constructors.Cls;

procedure Main
is
   use Test_Multiple_Custom_Constructors;
   use Interfaces.C;
   Value1, Value2 : Interfaces.C.int;
   D     : constant Interfaces.C.int := 78910;
   Class1 : aliased Cls.Class := Cls.Constructor (D);
   Class2 : aliased Cls.Class := Cls.Constructor (D, 10);
begin
   Value1 := Cls.Get_Value (Class1'Access);
   Tests.Assert (Value1 = 1234 + D, "Wrong value returned (1):" & Value1'Img);
   Value2 := Cls.Get_Value (Class2'Access);
   Tests.Assert (Value2 = 1234 + D - 10, "Wrong value returned (2):" & Value2'Img);
end Main;
