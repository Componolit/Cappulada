#include "impl.h"

template<typename T>
Cls<T>::Cls() { };

template<typename T>
Cls<T>::Cls(T val1) : _data(val1) { };

template<typename T>
void Cls<T>::get(T &val2) { val2 = _data; };

void Unused(char &c, int &i) {
   Foo::cls_inst1.get(c);
   Foo::cls_inst2.get(i);
}
