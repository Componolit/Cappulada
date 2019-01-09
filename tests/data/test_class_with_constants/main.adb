with Tests;
with Interfaces.C.Extensions;
with Test_Class_With_Constants.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Class_With_Constants;
   use Interfaces.C;
   use Interfaces.C.Extensions;

   C : Cls.Class := Cls.Constructor;
begin
   Tests.Assert (C.Constant_Int_Const = 15, "Wrong value returned (1): " & C.Constant_Int_Const'Img);
   Tests.Assert (C.Constant_Float_Const = 42.1, "Wrong value returned (2): " & C.Constant_Float_Const'Img);
   Tests.Assert (C.Constant_Bool_False_Const = False, "Wrong value returned (3)" & C.Constant_Bool_False_Const'Img);
   Tests.Assert (C.Constant_Bool_True_Const = True, "Wrong value returned (4)" & C.Constant_Bool_True_Const'Img);
   Tests.Assert (C.Constant_Ul_Const = 123456789, "Wrong value returned (5)" & C.Constant_Ul_Const'Img);
   Tests.Assert (C.Constant_Short_Const = -1234, "Wrong value returned (6)" & C.Constant_Short_Const'Img);
end Main;
