
template <typename T, int I> class T1 { };

template <typename U, int H> class T2
{
    public:
        T1<U, H> t1;
};

class T_int
{
    public:
        T2<int, 0> t2;
};
