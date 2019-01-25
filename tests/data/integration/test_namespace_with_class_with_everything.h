
namespace With_class
{
    class With_everything
    {
        public:
        enum {
            ONE = 1,
            TWO = 2
        };

        enum NEGATIVE {
            MINUS_ONE = -1,
            MINUS_TWO = -2
        };

        private:

        void private_function();
        int private_int;

        public:

        void public_function();
        int public_int;
        With_everything();
    };
}
