#include "impl.h"

Cls::Cls() : _value(0) { };
Cls::Cls(int val) : _value(val) { };
int Cls::cpp_method (int param) { return ada_method(param) + 7; };
