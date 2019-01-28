
#include <number.h>

Number::Number(int v) : _value(v)
{ }

void Number::add(int n)
{
    _value += n;
}

int Number::value()
{
    return _value;
}
