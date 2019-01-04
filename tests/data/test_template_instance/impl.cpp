#include "impl.h"

template<typename T>
Cls<T>::Cls() { };

template<typename T>
Cls<T>::Cls(T val) : _data(val) { };

template<typename T>
void Cls<T>::get(T &val) { val = _data; };
