with Ada.Unchecked_Conversion;
with Tests;
with Interfaces.C.Extensions;
with Test_Class_With_Class_Pointer_Member.Outer;
with Test_Class_With_Class_Pointer_Member.Inner;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Class_With_Class_Pointer_Member;
   use Interfaces.C;
   use Interfaces.C.Extensions;

   O : aliased Outer.Class := Outer.Constructor (37, 123456);
   I : Interfaces.C.int;

   type ICA is access Inner.Class;
   function Ptr is new Ada.Unchecked_Conversion(Inner.Class_Address, ICA);

begin
   Tests.Assert (O.Data = 37, "Wrong data (1): " & O.Data'Img);

   I := Outer.Get_Inner_Data (O);
   Tests.Assert (I = 123456, "Wrong data (2): " & I'Img);

   I := Inner.Get_Data (Ptr(O.Class_Data).all);
   Tests.Assert (I = 123456, "Wrong data (3): " & I'Img);
end Main;
