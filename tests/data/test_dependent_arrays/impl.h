
template <int S>
class Cls
{
    public:
        int ar[S];
        long pad;
        Cls()
        {
            for(int i = 0; i < S; i++){
                ar[i] = i;
            }
            pad = 42;
        }
};

namespace Hidden {
    Cls<3> Cls_3();
}
