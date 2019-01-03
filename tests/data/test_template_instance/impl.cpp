#include "impl.h"

Cls::Cls() { };

Cls::Cls(T val) : _data(val) { };

void Cls::get(T &val) { val = _data };
