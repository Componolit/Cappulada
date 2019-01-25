with System;
with Tests;
with Interfaces.C;
with Test_Member_Reference;
with Ada.Unchecked_Conversion;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Member_Reference;

   C1 : aliased Cls.Class  := Cls.Constructor;
   C2 : aliased Cls.Class  := Cls.Constructor (518);
   Val1, Val2 : Int;

   type IA is access all int;
   function To_Access is new Ada.Unchecked_Conversion (int_address, IA);
   use Interfaces.C;

begin
   Val1 := Cls.Method (C1);
   Tests.Assert (Val1 = 17, "Wrong value returned (1): " & Val1'Img);
   Tests.Assert (To_Access (C1.Ref).all = 16, "Wrong value returned (2): " & To_Access (C1.Ref).all'Img);

   Val2 := Cls.Method (C2);
   Tests.Assert (Val2 = 519, "Wrong value returned (3): " & Val2'Img);
   Tests.Assert (To_Access (C2.Ref).all = 518, "Wrong value returned (4): " & To_Access (C2.Ref).all'Img);
end Main;
