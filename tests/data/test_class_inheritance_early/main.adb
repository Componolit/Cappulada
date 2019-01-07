with Tests;
with Interfaces.C;
with Test_Class_Inheritance_Early.Base;
with Test_Class_Inheritance_Early.Cls;

procedure Main
is
   use Test_Class_Inheritance_Early;

   B : aliased Base.Class := Base.Constructor (56789);
   C : aliased Cls.Class  := Cls.Constructor (12345);

   Val1, Val2 : Int;
   use Interfaces.C;
begin
   Val1 := Base.Parent (B'Access);
   Tests.Assert (Val1 = 56789, "Wrong value returned (1): " & Val1'Img & " / " & B.Parent_Member'Img);

   Val2 := Cls.Local (C'Access);
   Tests.Assert (Val2 = 12345, "Wrong value returned (2): " & Val2'Img & " / " & C.Local_Member'Img);

end Main;
