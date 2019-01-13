#include "impl.h"

Cls::Cls() : func(nullptr) { };
void Cls::set_func(int (*arg)(int)) { func = arg; };
int Cls::use_func(int arg) { if (func) { return func(arg); } else { return 0; }; };
