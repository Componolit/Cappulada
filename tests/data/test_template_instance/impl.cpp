#include "impl.h"

template<typename T>
Cls<T>::Cls() { };

template<typename T>
Cls<T>::Cls(T val1) : _data(val1) { };

template<typename T>
void Cls<T>::get(T &val2) { val2 = _data; };

template<typename T>
T& Cls<T>::get() { return _data; };

void Unused(char &c, int &i, Cls<char> &cc, Cls<int> &ci) {
   cc = Cls<char>();
   Foo::cls_inst1.get(c);
   c = Foo::cls_inst1.get();

   ci = Cls<int>();
   Foo::cls_inst2.get(i);
   i = Foo::cls_inst2.get();
}
