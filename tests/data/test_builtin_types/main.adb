with Tests;
with Interfaces.C.Extensions;
with Test_Builtin_Types;
with Ada.Unchecked_Conversion;

procedure Main
   with SPARK_Mode => Off
is
   use Interfaces.C;
   use Interfaces.C.Extensions;

   B    : aliased bool;
   Uc   : aliased unsigned_char;
   Us   : aliased unsigned_short;
   U    : aliased unsigned;
   Ul   : aliased unsigned_long;
   Ull  : aliased unsigned_long_long;
   C    : aliased char;
   Sc   : aliased signed_char;
   Wct  : aliased wchar_t;
   S    : aliased short;
   I    : aliased int;
   I128 : aliased Signed_128;
   L    : aliased long;
   Ll   : aliased long_long;
   F    : aliased c_float;
   D    : aliased double;

   use Test_Builtin_Types;

   type BA is access all Test_Builtin_Types.bool;
   function To_Address is new Ada.Unchecked_Conversion (BA, Bool_Address);

   type UCA is access all Test_Builtin_Types.unsigned_char;
   function To_Address is new Ada.Unchecked_Conversion (UCA, Unsigned_Char_Address);

   type USA is access all Test_Builtin_Types.unsigned_short;
   function To_Address is new Ada.Unchecked_Conversion (USA, Unsigned_Short_Address);

   type UA is access all Test_Builtin_Types.unsigned_int;
   function To_Address is new Ada.Unchecked_Conversion (UA, Unsigned_Int_Address);

   type ULA is access all Test_Builtin_Types.unsigned_long;
   function To_Address is new Ada.Unchecked_Conversion (ULA, Unsigned_Long_Address);

   type ULLA is access all Test_Builtin_Types.unsigned_long_long;
   function To_Address is new Ada.Unchecked_Conversion (ULLA, Unsigned_Long_Long_Address);

   type CA is access all Test_Builtin_Types.char;
   function To_Address is new Ada.Unchecked_Conversion (CA, Char_Address);

   type SCA is access all Test_Builtin_Types.signed_char;
   function To_Address is new Ada.Unchecked_Conversion (SCA, Signed_Char_Address);

   type WCTA is access all Test_Builtin_Types.wchar_t;
   function To_Address is new Ada.Unchecked_Conversion (WCTA, Wchar_t_Address);

   type SA is access all Test_Builtin_Types.short;
   function To_Address is new Ada.Unchecked_Conversion (SA, Short_Address);

   type IA is access all Test_Builtin_Types.int;
   function To_Address is new Ada.Unchecked_Conversion (IA, Int_Address);

   type I128A is access all Test_Builtin_Types.C_X_Int128;
   function To_Address is new Ada.Unchecked_Conversion (I128A, C_X_Int128_Address);

   type LA is access all Test_Builtin_Types.long;
   function To_Address is new Ada.Unchecked_Conversion (LA, Long_Address);

   type LLA is access all Test_Builtin_Types.long_long;
   function To_Address is new Ada.Unchecked_Conversion (LLA, Long_Long_Address);

   type FA is access all Test_Builtin_Types.c_float;
   function To_Address is new Ada.Unchecked_Conversion (FA, C_Float_Address);

   type DA is access all Test_Builtin_Types.double;
   function To_Address is new Ada.Unchecked_Conversion (DA, Double_Address);

   Klass : aliased Cls.Class :=
      Cls.Constructor (True,
                       54,
                       6453,
                       549993,
                       9999993343,
                       32124452323,
                       'F',
                       55,
                       '#',
                       -123,
                       -4343559,
                       Signed_128'(53443, 3232),
                       434993434,
                       9999994334343,
                       32.4343,
                       -433434.1223);

begin
   Cls.Get (Klass,
            To_Address (B'Access),
            To_Address (Uc'Access),
            To_Address (Us'Access),
            To_Address (U'Access),
            To_Address (Ul'Access),
            To_Address (Ull'Access),
            To_Address (C'Access),
            To_Address (Sc'Access),
            To_Address (Wct'Access),
            To_Address (S'Access),
            To_Address (I'Access),
            To_Address (I128'Access),
            To_Address (L'Access),
            To_Address (Ll'Access),
            To_Address (F'Access),
            To_Address (D'Access));

   Tests.Assert (B    = True,                     "Wrong value returned  (1): " & B'Img);
   Tests.Assert (Uc   = 54,                       "Wrong value returned  (2): " & Uc'Img);
   Tests.Assert (Us   = 6453,                     "Wrong value returned  (3): " & Uc'Img);
   Tests.Assert (U    = 549993,                   "Wrong value returned  (4): " & U'Img);
   Tests.Assert (Ul   = 9999993343,               "Wrong value returned  (5): " & Ul'Img);
   Tests.Assert (Ull  = 32124452323,              "Wrong value returned  (6): " & Ull'Img);
   Tests.Assert (C    = 'F',                      "Wrong value returned  (7): " & C'Img);
   Tests.Assert (Sc   = 55,                       "Wrong value returned  (8): " & Sc'Img);
   Tests.Assert (Wct  = '#',                      "Wrong value returned  (9): " & Wct'Img);
   Tests.Assert (S    = -123,                     "Wrong value returned (10): " & S'Img);
   Tests.Assert (I    = -4343559,                 "Wrong value returned (11): " & I'Img);
   Tests.Assert (I128 = Signed_128'(53443, 3232), "Wrong value returned (12): " & I128.high'Img & "/" & I128.low'Img);
   Tests.Assert (L    = 434993434,                "Wrong value returned (13): " & L'Img);
   Tests.Assert (Ll   = 9999994334343,            "Wrong value returned (14): " & Ll'Img);
   Tests.Assert (F    = 32.4343,                  "Wrong value returned (15): " & F'Img);
   Tests.Assert (D    = -433434.1223,             "Wrong value returned (16): " & D'Img);
end Main;
