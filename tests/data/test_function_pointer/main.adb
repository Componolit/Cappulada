with Tests;
with Interfaces.C;
with Test_Function_Pointer.Cls;

procedure Main
   with SPARK_Mode => Off
is
   use Test_Function_Pointer;

   function Add15 (This : Cls.Class;
                   Arg1 : Test_Function_Pointer.int) return Test_Function_Pointer.int
   with Convention => Cpp;

   function Add15 (This : Cls.Class;
                   Arg1 : Test_Function_Pointer.int) return Test_Function_Pointer.int
   is
      use Interfaces.C;
   begin
      return Arg1 + 15;
   end Add15;

   C : Cls.Class := Cls.Constructor;
   Val : int;
   use Interfaces.C;

begin
   Cls.Set_Func (C, Add15'Access);
   Val := Cls.Use_Func (C, 15);
   Tests.Assert (Val = 30, "Wrong value returned (0): " & Val'Img);
end Main;
