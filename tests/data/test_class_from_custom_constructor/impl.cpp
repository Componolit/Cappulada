#include "impl.h"

Cls::Cls() : _delta(0) { };
Cls::Cls(int delta) : _delta(delta) { };

int Cls::get_value () {
   return _value + _delta;
}
