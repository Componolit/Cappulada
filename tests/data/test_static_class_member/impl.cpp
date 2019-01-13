#include "impl.h"

Cls::Cls() { };

Cls::Cls(int i, bool b)
   : int_member(i)
   , bool_member(b) { };

void Cls::set(short val) { Cls::static_short_member = val; };

short Cls::static_short_member;
