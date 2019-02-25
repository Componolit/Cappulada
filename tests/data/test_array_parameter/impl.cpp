
#include "impl.h"

Cls::Cls() { }

int Cls::sum(int list[], int length)
{
    int s = 0;
    for(int i = 0; i < length; i++){
        s += list[i];
    }
    return s;
}
