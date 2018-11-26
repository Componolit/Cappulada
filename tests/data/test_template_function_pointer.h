
template <typename T>
class With_Fptr
{
    public:
        void (T::*func) (void);
        void set_func(void (T::*func)(void));
};
