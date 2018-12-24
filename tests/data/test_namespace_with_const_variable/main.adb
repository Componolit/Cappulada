with Tests;
with Interfaces.C;
with Test_Namespace_With_Const_Variable.Constants.Cls;

procedure Main
is
   use Test_Namespace_With_Const_Variable;
   use Interfaces.C;
begin
   Tests.Assert (Constants.Int_Const = 42, "Constant has wrong value"); 
   Tests.Assert (Constants.Cls.Get_Const = 42, "Constant accessor returns wrong value"); 
end Main;
