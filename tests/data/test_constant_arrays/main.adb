with Tests;
with Test_Constant_Arrays;
with Interfaces.C;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Constant_Arrays.Cls;
   use all type Interfaces.C.Int;
   use all type Interfaces.C.Long;
   Inst : Class := Constructor;
begin
   Tests.Assert (Inst.Ar (1) = 0, "Array element 1 is " & Integer'Image (Integer (Inst.Ar (1))));
   Tests.Assert (Inst.Ar (2) = 1, "Array element 2 is " & Integer'Image (Integer (Inst.Ar (2))));
   Tests.Assert (Inst.Ar (3) = 2, "Array element 2 is " & Integer'Image (Integer (Inst.Ar (3))));
   Tests.Assert (Inst.Pad = 42, "Pad is " & Integer'Image (Integer (Inst.Pad)));
end Main;
