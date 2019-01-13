with Tests;
with Interfaces.C.Extensions;
with Test_Static_Class_Member.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Static_Class_Member;
   use Interfaces.C;
   use Interfaces.C.Extensions;

   C1 : Cls.Class := Cls.Constructor(5, False);
   C2 : Cls.Class := Cls.Constructor(10, True);
begin
   Cls.Set (C1, 34);
   Tests.Assert (C1.Int_Member = 5, "Wrong value returned (1): " & C1.Int_Member'Img);
   Tests.Assert (C1.Bool_Member = False, "Wrong value returned (2): " & C1.Bool_Member'Img);
   Tests.Assert (Cls.Static_Short_Member = 34, "Static member has wrong value (1): " & Cls.Static_Short_Member'Img);

   Cls.Set (C2, 8);
   Tests.Assert (C2.Int_Member = 10, "Wrong value returned (3): " & C2.Int_Member'Img);
   Tests.Assert (C2.Bool_Member = True, "Wrong value returned (4): " & C2.Bool_Member'Img);
   Tests.Assert (Cls.Static_Short_Member = 8, "Static member has wrong value (2): " & Cls.Static_Short_Member'Img);
end Main;
