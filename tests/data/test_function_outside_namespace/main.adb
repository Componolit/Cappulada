with Tests;
with Interfaces.C;
with Test_Function_Outside_Namespace;

procedure Main
is
   use Test_Function_Outside_Namespace;
   use Interfaces.C;
   Value : Interfaces.C.int;
begin
   Value := Func(100);
   Tests.Assert (Value = 142, "Wrong value returned:" & Value'Img);
end Main;
