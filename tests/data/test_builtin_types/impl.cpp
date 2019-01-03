#include "impl.h"

Cls::Cls() { };

Cls::Cls(bool b,
         unsigned char uc,
         unsigned short us,
         unsigned u,
         unsigned long ul,
         unsigned long long ull,
         char c,
         signed char sc,
         wchar_t wct,
         short s,
         int i,
         __int128 i128,
         long l,
         long long ll,
         float f,
         double d,
         long double ld)
         :
         bool_member(b),
         unsigned_char_member(uc),
         unsigned_short_member(us),
         unsigned_member(u),
         unsigned_long_member(ul),
         unsigned_long_long_member(ull),
         char_member(c),
         signed_char_member(sc),
         wchar_t_member(wct),
         short_member(s),
         int_member(i),
         int128_member(i128),
         long_member(l),
         long_long_member(ll),
         float_member(f),
         double_member(d),
         long_double_member(ld) { };

void Cls::get(bool &b,
              unsigned char &uc,
              unsigned short &us,
              unsigned &u,
              unsigned long &ul,
              unsigned long long &ull,
              char &c,
              signed char &sc,
              wchar_t &wct,
              short &s,
              int &i,
              __int128 &i128,
              long &l,
              long long &ll,
              float &f,
              double &d,
              long double &ld)
{
   b    = bool_member;
   uc   = unsigned_char_member;
   us   = unsigned_short_member;
   u    = unsigned_member;
   ul   = unsigned_long_member;
   ull  = unsigned_long_long_member;
   c    = char_member;
   sc   = signed_char_member;
   wct  = wchar_t_member;
   s    = short_member;
   i    = int_member;
   i128 = int128_member;
   l    = long_member;
   ll   = long_long_member;
   f    = float_member;
   d    = double_member;
   ld   = long_double_member;
};
