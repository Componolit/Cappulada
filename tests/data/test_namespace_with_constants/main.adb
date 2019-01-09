with Tests;
with Interfaces.C.Extensions;
with Test_Namespace_With_Constants.Constants;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Namespace_With_Constants;
   use Interfaces.C;
   use Interfaces.C.Extensions;
begin
   Tests.Assert (Constants.Int_Const = 15, "Wrong value returned (1): " & Constants.Int_Const'Img);
   Tests.Assert (Constants.Float_Const = 42.1, "Wrong value returned (2): " & Constants.Float_Const'Img);
   Tests.Assert (Constants.Bool_False_Const = False, "Wrong value returned (3)" & Constants.Bool_False_Const'Img);
   Tests.Assert (Constants.Bool_True_Const = True, "Wrong value returned (4)" & Constants.Bool_True_Const'Img);
   Tests.Assert (Constants.Ul_Const = 123456789, "Wrong value returned (5)" & Constants.Ul_Const'Img);
   Tests.Assert (Constants.Short_Const = -1234, "Wrong value returned (6)" & Constants.Short_Const'Img);
end Main;
