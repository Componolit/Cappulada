with Tests;
with Interfaces.C;
with Test_Multiple_Members_With_Private_Type;

procedure Main
   with SPARK_Mode => Off
is
begin
   --  No actual test, we only want to ensure that the same private type
   --  declaration is generated only once.
   null;
end Main;
