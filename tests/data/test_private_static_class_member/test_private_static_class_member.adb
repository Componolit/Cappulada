package body Test_Private_Static_Class_Member is

   package body Cls
   is
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

   end Cls;

end Test_Private_Static_Class_Member;
