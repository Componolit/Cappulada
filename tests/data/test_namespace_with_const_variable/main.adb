with Tests;
with Interfaces.C;
with Test_Namespace_With_Const_Variable.Constants;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Namespace_With_Const_Variable;
   use Interfaces.C;
   Class : aliased Constants.Cls.Class := Constants.Cls.Constructor;
begin
   Tests.Assert (Constants.Int_Const = 42, "Constant has wrong value");
   Tests.Assert (Constants.Cls.Get_Const (Class) = 42, "Constant accessor returns wrong value");
end Main;
