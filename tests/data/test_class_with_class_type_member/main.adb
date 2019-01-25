with Tests;
with Interfaces.C.Extensions;
with Test_Class_With_Class_Type_Member;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Class_With_Class_Type_Member;
   use Interfaces.C;
   use Interfaces.C.Extensions;

   O : aliased Outer.Class := Outer.Constructor (37, 123456);
   I : Interfaces.C.int;

begin
   Tests.Assert (O.Data = 37, "Wrong data (1): " & O.Data'Img);
   I := Outer.Get_Inner_Data (O);
   Tests.Assert (I = 123456, "Wrong data (2): " & I'Img);
end Main;
