package body Test_Private_Static_Class_Member.Cls is

   ---------
   -- Get --
   ---------

   function Get
     (This : Class)
      return Test_Private_Static_Class_Member.Short
   is
   begin
      return Static_Private;
   end Get;

end Test_Private_Static_Class_Member.Cls;
