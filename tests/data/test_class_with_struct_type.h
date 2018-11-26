
class With_Struct
{
    public:
        struct Ws;
        struct Ws2;

        Ws value;
        Ws2 *value2;

        struct Ws {
            int x;
        };
};
