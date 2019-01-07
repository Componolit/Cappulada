#include "impl.h"
#include <stdio.h>

Base::Base() { };
Base::Base(int val) : _member(val) { };
int Base::method() { return _member; };

Cls::Cls() : Base(1234) { };
int Cls::method() { return 42; };
