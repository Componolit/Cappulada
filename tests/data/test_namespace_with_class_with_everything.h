
namespace With_class
{
    class With_everything
    {
        enum {
            ONE = 1,
            TWO = 2
        };

        enum NEGATIVE {
            ONE = -1,
            TWO = -2
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
