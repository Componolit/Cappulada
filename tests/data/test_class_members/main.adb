with Tests;
with Interfaces.C.Extensions;
with Test_Class_Members;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Class_Members;
   use Interfaces.C;
   use Interfaces.C.Extensions;

   C : Cls.Class := Cls.Constructor(5, 12.54, False, 5434254543, 123);
begin
   Tests.Assert (C.Int_Member = 5, "Wrong value returned (1): " & C.Int_Member'Img);
   Tests.Assert (C.Float_Member = 12.54, "Wrong value returned (2): " & C.Float_Member'Img);
   Tests.Assert (C.Bool_Member = False, "Wrong value returned (3): " & C.Bool_Member'Img);
   Tests.Assert (C.Ul_Member = 5434254543, "Wrong value returned (4): " & C.Ul_Member'Img);
   Tests.Assert (C.Short_Member = 123, "Wrong value returned (5): " & C.Short_Member'Img);

   C.Short_Member := 543;
   C.Ul_Member := 88888888;
   C.Bool_Member := True;
   C.Float_Member := -5.345;
   C.Int_Member := -75345;

   Tests.Assert (C.Int_Member = -75345, "Wrong value returned (6): " & C.Int_Member'Img);
   Tests.Assert (C.Float_Member = -5.345, "Wrong value returned (7): " & C.Float_Member'Img);
   Tests.Assert (C.Bool_Member = True, "Wrong value returned (8): " & C.Bool_Member'Img);
   Tests.Assert (C.Ul_Member = 88888888, "Wrong value returned (9): " & C.Ul_Member'Img);
   Tests.Assert (C.Short_Member = 543, "Wrong value returned (10): " & C.Short_Member'Img);
end Main;
