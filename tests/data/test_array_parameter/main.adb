with Tests;
with Test_Array_Parameter;

procedure Main
   with SPARK_Mode => Off
is
   List : Test_Array_Parameter.Int_Array (1 .. 10) := (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
   C : aliased Test_Array_Parameter.Cls.Class := Test_Array_Parameter.Cls.Constructor;
   Sum : Integer;
begin
   Sum := Integer (Test_Array_Parameter.Cls.Sum (C, List, Test_Array_Parameter.Int (List'Length)));
   Tests.Assert (Sum = 55, "Wrong sum returned: " & Sum'Img);
end Main;
