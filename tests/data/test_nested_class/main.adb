with Tests;
with Interfaces.C;
with Test_Nested_Class.Outer;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Nested_Class;

   O : aliased Outer.Class := Outer.Constructor (559988);
   I : aliased Outer.Inner.Class := Outer.Inner.Constructor (12345);

   Val1, Val2 : Int;
   use Interfaces.C;
begin
   Val1 := Outer.Method (O);
   Tests.Assert (Val1 = 559988, "Wrong value returned (1): " & Val1'Img);
   Tests.Assert (O.Member = 559988, "Wrong value returned (2): " & O.Member'Img);

   Val2 := Outer.Inner.Method (I);
   Tests.Assert (Val2 = 12345, "Wrong value returned (3): " & Val2'Img);
   Tests.Assert (I.Member = 12345, "Wrong value returned (4): " & I.Member'Img);

end Main;
