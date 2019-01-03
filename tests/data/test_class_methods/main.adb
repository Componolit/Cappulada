with Tests;
with Interfaces.C.Extensions;
with Test_Class_Methods.Cls;

procedure Main
is
   use Interfaces.C;
   use Interfaces.C.Extensions;

   I : aliased int;
   F : aliased c_float;
   B : aliased bool;
   U : aliased unsigned_long;
   S : aliased short;

   use Test_Class_Methods;
   C : aliased Cls.Class := Cls.Constructor(5, 12.54, False, 5434254543, 123);
begin
   Cls.Get (C'Access, I'Access, F'Access, B'Access, U'Access, S'Access);
   Tests.Assert (I = 5, "Wrong value returned (1): " & I'Img);
   Tests.Assert (F = 12.54, "Wrong value returned (2): " & F'Img);
   Tests.Assert (B = False, "Wrong value returned (3): " & B'Img);
   Tests.Assert (U = 5434254543, "Wrong value returned (4): " & U'Img);
   Tests.Assert (S = 123, "Wrong value returned (5): " & S'Img);
end Main;
