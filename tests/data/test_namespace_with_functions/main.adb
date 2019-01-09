with Ada.Unchecked_Conversion;
with Tests;
with Interfaces.C.Extensions;
with Test_Namespace_With_Functions.Functions;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Namespace_With_Functions;
   Result : int;
   Tmp : aliased int;

   type IA is access all int;
   function To_Address is new Ada.Unchecked_Conversion (IA, Int_Address);
   use Interfaces.C;

begin
   Result := Functions.Add (12345);
   Tests.Assert (Result = 12346, "Wrong value returned (1): " & Result'Img);

   Tmp := -56789;
   Functions.Add_Ptr (To_Address (Tmp'Access));
   Tests.Assert (Tmp = -56788, "Wrong value returned (2): " & Tmp'Img);

end Main;
