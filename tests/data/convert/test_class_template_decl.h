
template <typename T> class T1 { };

template <typename T> class T2
{
    public:
        T1<T> t1;
};

class T_int
{
    public:
        T2<int> &t2;
};
