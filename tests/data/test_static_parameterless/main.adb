with Tests;
with Interfaces.C;
with Test_Static_Parameterless.Cls;

procedure Main
is
   use Test_Static_Parameterless;
   use Interfaces.C;
begin
   Tests.Assert (Cls.Parameterless = 45678, "Wrong value returned:" & Cls.Parameterless'Img);
end Main;
