
template <typename A, typename B>
class Container
{
    public:
        A a;
        B b;
};


class User
{
    public:
        Container<int, char> cic;
        Container<int, int> cii;
        Container<int, char> cic2;
};
