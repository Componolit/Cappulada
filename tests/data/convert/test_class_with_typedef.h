
class With_Typedef
{
    public:
        typedef int i32;
//        i32 value;
};

class Use_Typedef
{
    public:
        With_Typedef::i32 value;
};
