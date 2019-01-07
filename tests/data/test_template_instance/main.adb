with Tests;
with Interfaces.C;
with Test_Template_Instance.Cls_T_Int;
with Test_Template_Instance.Cls_T_Char;

procedure Main
is
   use Interfaces.C;
   Char_Val : aliased char;
   Int_Val  : aliased int;
   Char_Ref : access char;
   Int_Ref  : access int;

   use Test_Template_Instance;
   Char_Inst : aliased Cls_T_Char.Class := Cls_T_Char.Constructor ('X');
   Int_Inst  : aliased Cls_T_Int.Class  := Cls_T_Int.Constructor (12365345);
begin
   Cls_T_Char.Get (Char_Inst'Access, Char_Val'Access);
   Char_Ref := Cls_T_Char.Get (Char_Inst'Access);

   Cls_T_Int.Get (Int_Inst'Access, Int_Val'Access);
   Int_Ref := Cls_T_Int.Get (Int_Inst'Access);

   Tests.Assert (Char_Val = 'X', "Wrong value returned (1): " & Char_Val'Img);
   Tests.Assert (Char_Ref.all = 'X', "Wrong value returned (2): " & Char_Ref.all'Img);

   Tests.Assert (Int_Val = 12365345, "Wrong value returned (3): " & Int_Val'Img);
   Tests.Assert (Int_Ref.all = 12365345, "Wrong value returned (4): " & Int_Ref.all'Img);
end Main;
