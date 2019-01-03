#include "impl.h"

Inner::Inner() { };
Inner::Inner(int d) : data(d) { };

Outer::Outer() : class_data(new Inner()) { };
Outer::Outer(short d, int i) : data(d), class_data(new Inner(i)) { };

int Inner::get_data() { return data; };
int Outer::get_inner_data() { return class_data->get_data(); };
