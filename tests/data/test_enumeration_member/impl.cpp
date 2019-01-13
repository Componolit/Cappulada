#include "impl.h"

Cls::Cls() : data(Invalid) { };
Cls::Cls(Elements e) : data(e) { };

Elements Cls::get() { return data; };
void Cls::set(Elements e) { data = e; };
