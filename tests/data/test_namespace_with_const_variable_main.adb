with Ada.Command_Line;
with Ada.Text_IO;

with Test_Namespace_With_Const_Variable_Ada;

procedure Test_Namespace_With_Const_Variable_Main
is
   use Ada.Text_IO;
begin
   Put_Line ("FIXME: Test failed"); 
   Ada.Command_Line.Set_Exit_Status (1);
end Test_Namespace_With_Const_Variable_Main;
