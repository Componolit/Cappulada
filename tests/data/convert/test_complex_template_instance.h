
namespace A
{
    template <typename T, typename T1, int L, typename T2>
    class B{ };

    template <typename T1, typename T2>
    class C{ };

    template <typename T1, typename T2>
    class D{ };

    class E{ };
}

typedef A::C<char, char> A_Char_Char;

class I{
    public:
        A::B<int, A::C<int, A::D<int, A::E>>, 4, A_Char_Char> x;
};
