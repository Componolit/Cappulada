#include "impl.h"

Cls::Cls() { };
Cls::Cls(Element e) : data(e) { };

Elements Cls::get() { return data; };
void Cls::set(Element e) { data = e; };
