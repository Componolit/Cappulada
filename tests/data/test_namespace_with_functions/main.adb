with Tests;
with Interfaces.C.Extensions;
with Test_Namespace_With_Functions.Functions;

procedure Main
is
   use Test_Namespace_With_Functions;
   Result : int;
   Tmp : Int_Address := new int;
   use Interfaces.C;
begin
   Result := Functions.Add (12345);
   Tests.Assert (Result = 12346, "Wrong value returned (1): " & Result'Img);

   Tmp.all := -56789;
   Functions.Add_Ptr (Tmp);
   Tests.Assert (Tmp.all = -56788, "Wrong value returned (2): " & Tmp.all'Img);

end Main;
