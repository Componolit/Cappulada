with Tests;
with Interfaces.C.Extensions;
with Test_Builtin_Types.Cls;

procedure Main
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
   Ld   : aliased long_double;

   use Test_Builtin_Types;
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
                       -433434.1223,
                       593430024.559);

begin
   Cls.Get (Klass'Access, B'Access, Uc'Access, Us'Access, U'Access, Ul'Access, Ull'Access, C'Access, Sc'Access,
            Wct'Access, S'Access, I'Access, I128'Access, L'Access, Ll'Access, F'Access, D'Access, Ld'Access);
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
   Tests.Assert (Ld   = 593430024.559,            "Wrong value returned (17): " & Ld'Img);
end Main;
