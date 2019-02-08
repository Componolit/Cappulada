
template <int S>
class Cls
{
    public:
        int ar[S];
};

namespace Dummy {
    Cls<3> c3;
}
