with Tests;
with Interfaces.C.Extensions;
with Test_Class_Methods.Cls;
with Ada.Unchecked_Conversion;

procedure Main
   with SPARK_Mode => Off
is
   use Interfaces.C;
   use Interfaces.C.Extensions;

   I : aliased int;
   F : aliased c_float;
   B : aliased bool;
   U : aliased unsigned_long;
   S : aliased short;

   type IA is access all int;
   type FA is access all c_float;
   type BA is access all bool;
   type UA is access all unsigned_long;
   type SA is access all short;

   use Test_Class_Methods;

   function To_Address is new Ada.Unchecked_Conversion (IA, int_address);
   function To_Address is new Ada.Unchecked_Conversion (FA, c_float_address);
   function To_Address is new Ada.Unchecked_Conversion (BA, bool_address);
   function To_Address is new Ada.Unchecked_Conversion (UA, unsigned_long_address);
   function To_Address is new Ada.Unchecked_Conversion (SA, short_address);

   C : aliased Cls.Class := Cls.Constructor(5, 12.54, False, 5434254543, 123);

begin
   Cls.Get (C, To_Address(I'Access), To_Address(F'Access), To_Address(B'Access), To_Address(U'Access), To_Address(S'Access));
   Tests.Assert (I = 5, "Wrong value returned (1): " & I'Img);
   Tests.Assert (F = 12.54, "Wrong value returned (2): " & F'Img);
   Tests.Assert (B = False, "Wrong value returned (3): " & B'Img);
   Tests.Assert (U = 5434254543, "Wrong value returned (4): " & U'Img);
   Tests.Assert (S = 123, "Wrong value returned (5): " & S'Img);
end Main;
