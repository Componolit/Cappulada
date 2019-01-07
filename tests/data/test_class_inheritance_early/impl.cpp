#include "impl.h"
#include <stdio.h>

Base::Base() { };
Base::Base(int val) : parent_member(val) { };
int Base::parent() { return parent_member; };

Cls::Cls() { };
Cls::Cls(int val) : Base(val+1), local_member(val) { };
int Cls::local() { return local_member; };
