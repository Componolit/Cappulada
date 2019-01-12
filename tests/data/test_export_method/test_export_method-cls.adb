package body Test_Export_Method.Cls
is
   function Ada_Method (This : Class; Param : Test_Export_Method.Int) return Test_Export_Method.Int
   is
      use type Interfaces.C.int;
   begin
      return int (This.Private_X_Value) + Param;
   end Ada_Method;

end Test_Export_Method.Cls;
