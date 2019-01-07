#include "impl.h"

int r1, r2;

Cls::Cls() : ref(r1) { ref = 16; };
Cls::Cls(int val) : ref(r2) { ref = val; };

int Cls::method() {
   return ref + 1;
}
