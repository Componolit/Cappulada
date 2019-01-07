#include "impl.h"

Cls::Cls() { };
Cls::Cls(int val) : member(val), ptr(&val) { };

int Cls::method() {
   return *ptr + 1;
}
