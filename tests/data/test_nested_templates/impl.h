
template <typename T>
class T1
{
    public:
        T m1;
        char m2;
        T1()
        {
            m1 = 42;
            m2 = '1';
        }
};

template <typename T>
class T2
{
    public:
        T1<T> m1;
        char m2;
        T2() : m1()
        {
            m2 = '2';
        }
};

class Inst
{
    public:
        T2<int> t_int;
        Inst();
};
