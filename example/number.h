

template <typename T>
class Number
{
    private:
        T _value;
    public:
        Number(T v) : _value(v)
        { }

        void add(T n)
        {
            _value += n;
        }

        T value()
        {
            return _value;
        }
};

class Dummy{
    public:
        Dummy(Number<int> n)
        {
            n.add(1);
            n.value();
        }
};
