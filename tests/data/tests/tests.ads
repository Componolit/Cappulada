package Tests
   with SPARK_Mode
is
   procedure Assert
     (Condition : Boolean;
      Message   : String;
      Status    : Natural := 1);

end Tests;
