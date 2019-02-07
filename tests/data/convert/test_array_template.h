
template <int Size>
class Template_With_Array
{
    public:
        int var[Size];
};

class With_Array_5
{
    public:
        Template_With_Array<5> twa;
};
