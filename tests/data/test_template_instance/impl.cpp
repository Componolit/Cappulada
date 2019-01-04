#include "impl.h"

template<typename T>
Cls<T>::Cls() { };

template<typename T>
Cls<T>::Cls(T val) : _data(val) { };

template<typename T>
void Cls<T>::get(T &val) { val = _data; };

void Unused(char &c, int &i) {
   Foo::cls_inst1.get(c);
   Foo::cls_inst2.get(i);
}
