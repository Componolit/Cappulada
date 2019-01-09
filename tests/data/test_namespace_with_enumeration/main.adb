with Ada.Unchecked_Conversion;
with Tests;
with Interfaces.C.Extensions;
with Test_Namespace_With_Enumeration.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Namespace_With_Enumeration.Cls;
   type Raw_Days is mod 2**Numbered_Days'Size;
   function To_Int is new Ada.Unchecked_Conversion (Numbered_Days, Raw_Days);

   type Raw_Tage is mod 2**(Tage'Size);
   function To_Int is new Ada.Unchecked_Conversion (Tage, Raw_Tage);
begin
   Tests.Assert (To_Int (Monday)    =  17, "Element has wrong value (1): " & Monday'Img);
   Tests.Assert (To_Int (Tuesday)   =  23, "Element has wrong value (2): " & Tuesday'Img);
   Tests.Assert (To_Int (Wednesday) = 111, "Element has wrong value (3): " & Wednesday'Img);
   Tests.Assert (To_Int (Thursday)  =   5, "Element has wrong value (4): " & Thursday'Img);
   Tests.Assert (To_Int (Friday)    =  10, "Element has wrong value (5): " & Friday'Img);
   Tests.Assert (To_Int (Saturday)  =   1, "Element has wrong value (6): " & Saturday'Img);
   Tests.Assert (To_Int (Sunday)    = 654, "Element has wrong value (7): " & Sunday'Img);

   Tests.Assert (To_Int (Montag)     = 0, "Element has wrong value (8): " &  To_Int (Montag)'Img);
   Tests.Assert (To_Int (Dienstag)   = 1, "Element has wrong value (9): " &  To_Int (Dienstag)'Img);
   Tests.Assert (To_Int (Mittwoch)   = 2, "Element has wrong value (A): " &  To_Int (Mittwoch)'Img);
   Tests.Assert (To_Int (Donnerstag) = 3, "Element has wrong value (B): " &  To_Int (Donnerstag)'Img);
   Tests.Assert (To_Int (Freitag)    = 4, "Element has wrong value (C): " &  To_Int (Freitag)'Img);
   Tests.Assert (To_Int (Sonnabend)  = 5, "Element has wrong value (D): " &  To_Int (Sonnabend)'Img);
   Tests.Assert (To_Int (Sonntag)    = 6, "Element has wrong value (E): " &  To_Int (Sonntag)'Img);
end Main;
