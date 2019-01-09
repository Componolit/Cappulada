with Ada.Unchecked_Conversion;
with Tests;
with Interfaces.C;
with Test_Template_Instance.Cls_T_Int;
with Test_Template_Instance.Cls_T_Char;

procedure Main
   with SPARK_Mode => Off
is
   use Interfaces.C;
   Char_Val : aliased char;
   Int_Val  : aliased int;

   type CA is access all char;
   type IA is access all int;

   use Test_Template_Instance;
   Char_Inst : aliased Cls_T_Char.Class := Cls_T_Char.Constructor ('X');
   Int_Inst  : aliased Cls_T_Int.Class  := Cls_T_Int.Constructor (12365345);

   Char_Addr : Char_Address;
   Int_Addr  : Int_Address;

   function To_Address is new Ada.Unchecked_Conversion (CA, Char_Address);
   function To_Access is new Ada.Unchecked_Conversion (Char_Address, CA);

   function To_Address is new Ada.Unchecked_Conversion (IA, Int_Address);
   function To_Access is new Ada.Unchecked_Conversion (Int_Address, IA);

begin
   Cls_T_Char.Get (Char_Inst, To_Address (Char_Val'Access));
   Char_Addr := Cls_T_Char.Get (Char_Inst);

   Cls_T_Int.Get (Int_Inst, To_Address (Int_Val'Access));
   Int_Addr := Cls_T_Int.Get (Int_Inst);

   Tests.Assert (Char_Val = 'X', "Wrong value returned (1): " & Char_Val'Img);
   Tests.Assert (To_Access (Char_Addr).all = 'X', "Wrong value returned (2): " & To_Access (Char_Addr).all'Img);

   Tests.Assert (Int_Val = 12365345, "Wrong value returned (3): " & Int_Val'Img);
   Tests.Assert (To_Access (Int_Addr).all = 12365345, "Wrong value returned (4): " & To_Access (Int_Addr).all'Img);
end Main;
