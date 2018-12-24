with Ada.Text_IO;
with GNAT.OS_Lib;

package body Tests is

   ------------
   -- Assert --
   ------------

   procedure Assert
     (Condition : Boolean;
      Message   : String;
      Status    : Natural := 1)
   is
   begin
      if not Condition
      then
         Ada.Text_IO.Put_Line ("ERROR: " & Message);
         GNAT.OS_Lib.OS_Exit (Status);
      end if;
   end Assert;

end Tests;
