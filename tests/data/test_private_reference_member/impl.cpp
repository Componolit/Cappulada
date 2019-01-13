#include "impl.h"

int defval = 42;

Privref::Privref() : member(defval) { };

Privref::Privref(int val) : member(val) { };

int Privref::get() { return member; };
