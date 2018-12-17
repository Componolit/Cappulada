
template <typename T1>
class Template1
{
    public:
        T1 value;
};


template <typename T2>
class Template2
{
    public:
        void func(Template1<T2> t);
};

class Tint
{
    public:
        Template2<int> value;
};

