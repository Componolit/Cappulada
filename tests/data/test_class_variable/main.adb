with Tests;
with Interfaces.C.Extensions;
with Test_Class_Variable.Foo;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Class_Variable;
   use Interfaces.C;
begin
   -- Tests.Assert (Cls_Inst1.Value = 17, "Wrong value returned (1): " & Cls_Inst1.Value'Img);
   Tests.Assert (Foo.Cls_Inst2.Value = 17, "Wrong value returned (2): " & Foo.Cls_Inst2.Value'Img);
end Main;
