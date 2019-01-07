#include "impl.h"

Outer::Outer() { };
Outer::Outer(int val) : member(val) { };
int Outer::method() { return member; };

Outer::Inner::Inner() { };
Outer::Inner::Inner(int val) : member(val) { };
int Outer::Inner::method() { return member; };
