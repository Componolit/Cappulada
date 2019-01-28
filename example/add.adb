with Ada.Command_Line;
with Ada.Text_Io;
with Example;
with Example.Number;

procedure Add is

   function Number_Add (X : Integer; Y : Integer) return Integer is
      A : Example.Number.Class := Example.Number.Constructor (Example.Int(X));
   begin
      Example.Number.Add (A, Example.Int (Y));
      return Integer(Example.Number.Value (A));
   end Number_Add;

begin
   if Ada.Command_Line.Argument_Count = 2 then
      Ada.Text_Io.Put_Line (Integer'Image (Number_Add (
         Integer'Value (Ada.Command_Line.Argument(1)),
         Integer'Value (Ada.Command_Line.Argument(2))
         )));
   end if;
end Add;
