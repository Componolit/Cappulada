#include "impl.h"

Cls::Cls() { };

Cls::Cls(void *val) : _data(val) { };

void *Cls::get() { return _data; };
