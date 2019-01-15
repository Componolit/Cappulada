with Interfaces.C;
with Test_Namespace_With_Typedefs.With_Typedef;

procedure Main
is
   use Test_Namespace_With_Typedefs;
   use Interfaces.C;
   X : With_Typedef.U8 := 5;
   Y : With_Typedef.I32 := -154;
begin
   --  Just testing correct generation of types
   null;
end Main;
