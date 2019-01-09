with Tests;
with Interfaces.C.Extensions;
with Test_Complex_Class_Layout.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Complex_Class_Layout;
   use Interfaces.C;
   use Interfaces.C.Extensions;
   Class : aliased Cls.Class := Cls.Constructor (Val1 => 'x',
                                                 Val2 => 738583,
                                                 Val3 => 53.2353,
                                                 Val4 => '^',
                                                 Val5 => 1234567890123,
                                                 Val6 => '~');
begin
   Tests.Assert (Class.Val1 = 'x', "Class has wrong value (1): " & Class.Val1'Img);
   Tests.Assert (Class.Val2 = 738583, "Class has wrong value (2): " & Class.Val2'Img);
   Tests.Assert (Class.Val3 = 53.2353, "Class has wrong value (3): " & Class.Val3'Img);
   Tests.Assert (Class.Val4 = '^', "Class has wrong value (4): " & Class.Val4'Img);
   Tests.Assert (Class.Val5 = 1234567890123, "Class has wrong value (5): " & Class.Val5'Img);
   Tests.Assert (Class.Val6 = '~', "Class has wrong value (6): " & Class.Val6'Img);
end Main;
