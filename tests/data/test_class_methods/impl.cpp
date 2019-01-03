#include "impl.h"

Cls::Cls() { };

Cls::Cls(int i, float f, bool b, unsigned long ul, short s)
   : int_member(i)
   , float_member(f)
   , bool_member(b)
   , ul_member(ul)
   , short_member(s) { };

void Cls::get(int& i, float& f, bool& b, unsigned long& ul, short& s) {
   i = int_member;
   f = float_member;
   b = bool_member;
   ul = ul_member;
   s = short_member;
}
