#include "impl.h"

Base::Base() { };

int Base::method() { return 100; };
int Base::pure() { return 101; };
int Base::original() { return 103; };

int Cls::method() { return 42; };
int Cls::pure() { return 43; };
int Cls::own() { return 44; };

Cls::Cls() { };
