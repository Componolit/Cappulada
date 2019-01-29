
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

namespace temp{
    void dummy(){
        Number<int> n = Number<int>(1);
        n.add(1);
        n.value();
    }
}
