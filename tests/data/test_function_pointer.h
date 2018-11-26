
class With_Fptr
{
    public:
        void (*func) (void);
        void set_func(void (*func)(void));
};
