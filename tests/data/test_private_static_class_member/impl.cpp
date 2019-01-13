#include "impl.h"

Cls::Cls() { };

void Cls::set(short val) { Cls::static_private = val; };

short Cls::static_public;
short Cls::static_private;
