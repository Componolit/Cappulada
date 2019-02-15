
with Tests;
with Interfaces.C;
with Test_Nested_Templates;

procedure Main
   with SPARK_Mode => Off
is
   use Interfaces.C;
   use Test_Nested_Templates;
   I : Inst.Class := Inst.Constructor;
begin
   Tests.Assert (I.T_Int.M2 = '2', "Wrong T2 Character: " & Character(I.T_Int.M2));
   Tests.Assert (I.T_Int.M1.M2 = '1', "Wrong T1 Character: " & Character(I.T_Int.M1.M2));
   Tests.Assert (I.T_Int.M1.M1 = 42, "Wrong T1 Int: " & I.T_Int.M1.M1'Img);
end Main;
