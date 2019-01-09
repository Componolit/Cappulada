with Tests;
with Interfaces.C;
with Test_Class_Inheritance_Early_Overloaded.Base;
with Test_Class_Inheritance_Early_Overloaded.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Class_Inheritance_Early_Overloaded;

   B : aliased Base.Class := Base.Constructor (56789);
   C : aliased Cls.Class  := Cls.Constructor;

   Val1, Val2, Val3 : Int;
   use Interfaces.C;
begin
   Val1 := Base.Method (B);
   Tests.Assert (Val1 = 56789, "Wrong value returned (1): " & Val1'Img);

   Val2 := Cls.Method (C);
   Tests.Assert (Val2 = 42, "Wrong value returned (2): " & Val2'Img);

   --  Use parent method
   Val3 := Base.Method (C.Base);
   Tests.Assert (Val3 = 1234, "Wrong value returned (3): " & Val3'Img);

end Main;
