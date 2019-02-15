
template <typename T>
class T1 { };

template <typename U>
class T2
{
    public:
        T1<U> t1;
};

template <typename V>
class T3
{
    public:
        T2<V> t2;
};

template <typename W>
class T4
{
    public:
        T3<W> t3;
};

class Inst
{
    public:
        T4<int> t4_int;
        T4<char> t4_char;
};
