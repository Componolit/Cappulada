#include "impl.h"

Inner::Inner() { };
Inner::Inner(int d) : data(d) { };

Outer::Outer() { };
Outer::Outer(short d, int i) : class_data(i), data(d) { };

int Inner::get_data() { return data; };

int Outer::get_inner_data() { return class_data.get_data(); };
